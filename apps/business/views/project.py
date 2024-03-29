from django.db.models import Q

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from business.models.project import Project, ProjectFee, ProjectRejectReason
from business.models.task import Task
from points.models.projectpoints import ProjectPoints
from points.models.pointsdetail import PointsDetail
from points.models.points import Points
from configuration.models.project_conf import ProjectStatus, Fee
from configuration.models.task_conf import TaskType, TaskAssessment
from rbac.models import UserProfile

from business.serializers.project_serializer import (
    ProjectListSerializer, ProjectRejectReasonSerializer, ProjectFeeSerializer, ProjectReceiverListSerializer,
    ProjectSerializer, ProjectAuditorListSerializer)
from business.views.base import BusinessPublic
from business.filters import ProjectFilter

from common.custom import CommonPagination
from utils.basic import MykeyResponse

# 项目人员成本
list_project_person_objects = []
# 项目费用成本
list_project_fee_objects = []


class ProjectViewSet(ModelViewSet):
    """
    项目：增删改查
    """

    queryset = Project.objects.all()
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    filterset_class = ProjectFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def create(self, request, *args, **kwargs):
        self.before_create(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def before_create(self, request):
        # 将当前登录用户作为项目创建人
        request.data['sender'] = request.user.id

        receiver_id = request.data.get('receiver', None)
        # 如果存在项目负责人，则将项目接收状态置为 '待接手'
        if receiver_id is not None:
            BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2, messages='你有新的项目等待接手!')
            request.data['receive_status'] = ProjectStatus.objects.get(key='wait_accept').id
        # 如果不存在项目负责人，则将项目接手状态置为 '未指派项目负责人'
        else:
            request.data['receive_status'] = ProjectStatus.objects.get(key='unassigned').id

    def update(self, request, *args, **kwargs):
        self.before_update(request, kwargs)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def before_update(self, request, kwargs):
        project_id = str(kwargs['pk'])
        receiver_id = request.data.get('receiver', None)
        if receiver_id is not None and receiver_id != '':
            if project_id is not None:
                project = Project.objects.get(id=project_id)
                if project.receiver:
                    # 如果是驳回状态，需要重新发送消息
                    if receiver_id == str(project.receiver.id) and project.receive_status.id == 5:
                        # 新增消息
                        BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2,
                                                      messages='你有新的项目等待接手!')
                    elif receiver_id != str(project.receiver.id):
                        # 新增消息
                        BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2,
                                                      messages='你有新的项目等待接手!')
                else:
                    BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2,
                                                  messages='你有新的项目等待接手!')
            request.data['receive_status'] = ProjectStatus.objects.get(key='wait_accept').id
        else:
            request.data['receive_status'] = ProjectStatus.objects.get(key='unassigned').id

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_active=1).order_by('-add_time')

        queryset = self.filter_list_queryset(request, queryset)

        queryset = self.filter_project(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = 0
        instance.save()

        # self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def filter_project(self, request, queryset):
        """
        根据前端传递的查询参数过滤对应的项目
        :param request:
        :param queryset:
        :return:
        """
        q = Q()

        receive_status_ids = request.query_params.get('receive_status_ids', None)
        if receive_status_ids:
            receive_status_ids = receive_status_ids.split(',')
            q.add(Q(receive_status__in=receive_status_ids), Q.AND)

        audit_status_ids = request.query_params.get('audit_status_ids', None)
        if audit_status_ids:
            audit_status_ids = audit_status_ids.split(',')
            q.add(Q(audit_status__in=audit_status_ids), Q.AND)

        queryset = queryset.filter(q)

        return queryset

    def filter_list_queryset(self, request, queryset):
        """
        根据用户所属角色过滤查询集
        :param request:
        :param queryset:
        :return:
        """
        # 过滤已激活的项目数据
        queryset = queryset.filter(is_active=1)

        # 定义空的数据集
        emptyQuerySet = self.queryset.filter(is_active=999)
        queryset_project_auditor = emptyQuerySet
        queryset_project_manager = emptyQuerySet
        queryset_business_manager = emptyQuerySet

        # 获取当前用户 id
        user_id = request.user.id
        # 获取当前用户所属角色 id 列表
        user_role_ids = self.get_user_roles(user_id)

        # 如果当前用户拥有管理员权限，则不做特殊处理
        if 1 in user_role_ids:
            pass
        else:
            # 如果当前用户拥有项目审核员权限，则返回与该审核员关联的项目数据
            if 5 in user_role_ids:
                queryset_project_auditor = queryset.filter(auditor_id=user_id)
            # 如果当前用户拥有项目负责人权限，则返回与该项目负责人关联的项目数据
            if 7 in user_role_ids:
                queryset_project_manager = queryset.filter(receiver_id=user_id)
            # 如果当前用户拥有商务人员权限，则返回与该商务人员关联的项目数据
            if 8 in user_role_ids:
                queryset_business_manager = queryset.filter(sender_id=user_id)

            queryset = queryset_project_auditor | queryset_project_manager | queryset_business_manager

        return queryset

    def get_user_roles(self, user_id):
        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)
            user_roles = user.roles.all()
            user_role_ids = set(map(lambda user_role: user_role.id, user_roles))
            return user_role_ids


class ProjectNameView(APIView):
    """
    判断项目名是否已存在
    """

    def post(self, request, format=None):
        name = request.data.get('name', None)
        project_id = request.data.get('project_id', None)

        if project_id is not None:
            cur_project = Project.objects.get(id=project_id)
            if name == cur_project.name:
                return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')

        if name is not None:
            try:
                Project.objects.get(name=name)
                return MykeyResponse(status=status.HTTP_200_OK, data={'msg': '该项目名已存在，请重新输入'}, msg='请求成功')
            except Exception as e:
                return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')
        return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')


class ProjectReceiverListView(ListAPIView):
    """
    选择项目负责人
    """

    queryset = UserProfile.objects.filter(roles__id=7)
    serializer_class = ProjectReceiverListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectAuditorListView(ListAPIView):
    """
    获取所有项目审核员
    """

    queryset = UserProfile.objects.filter(roles__id=5)
    serializer_class = ProjectAuditorListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectFeeViewSet(ModelViewSet):
    """
    项目费用：增删改查
    """

    queryset = ProjectFee.objects.all()
    serializer_class = ProjectFeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('project_id',)
    ordering_fields = ('id',)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        self.before_list(request)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def before_list(self, request):
        project_id = request.query_params.get('project_id', None)
        is_first = request.query_params.get('is_first', None)
        if is_first == 'true' and project_id is not None:
            self.create_project_fee(project_id)

    def create_project_fee(self, project_id):
        fees = Fee.objects.all()
        for fee in fees:
            projectfee = ProjectFee.objects.filter(project_id=project_id, name=fee.name)
            if not projectfee.exists():
                project_fee_create = ProjectFee(
                    project_id=project_id,
                    name=fee.name,
                    value=fee.value,
                )
                project_fee_create.save()


class ProjectRejectReasonViewSet(ModelViewSet):
    """
    项目拒绝原因：增删改查
    """

    queryset = ProjectRejectReason.objects.all()
    serializer_class = ProjectRejectReasonSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ('-add_time',)
    filterset_fields = ('project_id',)
    permission_classes = (IsAuthenticated,)


class ProjectAuditSubmitView(APIView):
    """
    商务人员项目审核提交
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id')
            auditor_id = request.data.get('auditor_id')

            if project_id is not None and auditor_id is not None:
                self.update_project(project_id, auditor_id)
                user_id = request.user.id
                BusinessPublic.create_message(user_id, auditor_id, menu_id=2,
                                              messages='有新的项目需要你的审核，请尽快处理!')

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, auditor_id):
        """
        更新项目审核信息
        """

        project = Project.objects.get(id=project_id)
        if project:
            auditor = UserProfile.objects.get(id=auditor_id)
            project.auditor = auditor
            # 审核中
            project.audit_status = 1
            project.save()


class ProjectAuditPassView(APIView):
    """
    商务人员项目审核通过
    """

    def post(self, request, format=None):
        try:
            project_ids = request.data.get('project_ids', [])
            self.update_project(project_ids)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_ids):
        if len(project_ids) > 0:
            for project_id in project_ids:
                project = Project.objects.get(id=project_id)
                if project.receiver is None:
                    raise Exception('未填写项目负责人!')
                # 已审核
                project.audit_status = 2
                project.save()

                BusinessPublic.create_message(
                    project.auditor.id, project.receiver.id,
                    menu_id=2, messages='项目已通过审核!'
                )


class ProjectAuditRejectView(APIView):
    """
    商务人员项目审核驳回
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id')
            reason = request.data.get('reason') or ''

            self.update_project(project_id, reason)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        project = Project.objects.get(id=project_id)
        if project:
            # 驳回
            project.audit_status = 3
            project.save()

            BusinessPublic.create_reason(project.id, project.auditor.id, project.sender.id,
                                         BusinessPublic.GetReasonTypeIdByKey('project_audit_reject'),
                                         reason)
            BusinessPublic.create_message(project.auditor.id, project.sender.id, menu_id=2,
                                          messages='你的项目已被驳回，请尽快处理!')


class ProjectAcceptView(APIView):
    """
    接手项目
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id', None)
            if project_id is not None:
                self.update_project(project_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id):
        project = Project.objects.get(id=project_id)
        if project:
            # 项目负责人已接手,项目正式开始
            project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('accepted')
            project.save()
            BusinessPublic.create_message(project.receiver_id, project.sender_id, menu_id=2,
                                          messages='项目负责人已接手!')


class ProjectRejectView(APIView):
    """
    项目拒接
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id', None)
            # 驳回原因
            reason = request.data.get('reason', '')

            if project_id is not None:
                self.update_project(project_id, reason)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        project = Project.objects.get(id=project_id)
        if project is not None:
            # 拒接
            project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('rejected')
            project.save()

            reason_type_id = BusinessPublic.GetReasonTypeIdByKey('project_reject')

            BusinessPublic.create_reason(project.id, project.receiver.id, project.sender.id, reason_type_id, reason)
            BusinessPublic.create_message(project.receiver.id, project.sender.id, menu_id=2,
                                          messages='项目负责人拒接了你的项目，请尽快处理!')


class ProjectCheckSubmitView(APIView):
    """
    项目验收提交
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')

            self.update_project(project_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                # 验收提交
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('wait_check')
                project.save()

                BusinessPublic.create_message(project.receiver.id, project.auditor.id, menu_id=2,
                                              messages='该项目已完成，等待你的验收，请尽快处理!')


class ProjectCheckRejectView(APIView):
    """
    项目验收不通过
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')
            # 验收不通过原因
            reason = request.data.get('reason') or ''

            self.update_project(project_id, reason)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                # 验收不通过
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('check_rejected')
                project.save()

                BusinessPublic.create_reason(project.id, project.receiver.id, project.auditor.id,
                                             BusinessPublic.GetReasonTypeIdByKey('project_check_reject'),
                                             reason)
                BusinessPublic.create_message(project.receiver.id, project.auditor.id, menu_id=2,
                                              messages='你的项目验收不通过，请尽快检查!')


class ProjectCheckPassView(APIView):
    """
    项目验收成功
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')

            self.update_project(project_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                # 验收成功
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('checked')
                project.save()

                # 商务人员以及项目经理积分及米值分配
                projectpoints = ProjectPoints.objects.filter(project_id=project_id, task__isnull=True, is_created=0)
                if projectpoints:
                    for projectpoint in projectpoints:
                        if projectpoint:
                            self.create_user_points(None, projectpoint.user.id, projectpoint.points, 1, 1,
                                                    projectpoint.type)
                            project_points = ProjectPoints.objects.get(id=projectpoint.id)
                            project_points.is_created = 1
                            project_points.save()

                # 任务负责人积分及米值分配
                taskpoints = Task.objects.filter(project_id=project_id, is_active=1)
                if taskpoints:
                    for taskpoint in taskpoints:
                        if taskpoint:
                            self.create_user_points(taskpoint.task.id, taskpoint.receiver.id, taskpoint.points, 1, 1, 1)

                BusinessPublic.create_message(project.auditor_id, project.receiver_id, menu_id=2,
                                              messages='恭喜,你的项目已验收通过!')

    def create_user_points(self, task_id, user_id, point, operation_type, points_status, points_type):
        """
        创建或更新用户积分以及米值,如果用户积分表中存在记录则更新,如果没有则新增
        :param task_id:用户标识
        :param user_id:用户标识
        :param points:积分
        :param operation_type:操作类型：（1：增加积分或0：减少积分）
        :param points_status:积分状态：（1：有效）
        :param points_type:积分类型：（1：项目送或2：任务送）
        :return:
        """

        total_points = point
        available_points = point
        total_coins = round(total_points / 1000, 3)

        # 任务最终积分
        if task_id is not None:
            total_points = self.user_total_points(task_id, point)

        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)

            user_points = Points.objects.filter(user_id=user_id)
            if user_points.exists():
                user_point = Points.objects.get(user_id=user_id)
                user_point.user = user

                user_point.total_points = user_point.total_points + total_points
                user_point.available_points = user_point.available_points + total_points
                total_coins = round(total_points / 1000, 3)
                user_total_coins = round(user_point.total_coins, 3)
                user_point.total_coins = user_total_coins + total_coins
                user_point.save()

                self.create_user_pointsdetail(user_id, total_points, operation_type, points_status, points_type)
            else:
                Points.objects.create(user=user, total_points=total_points, available_points=available_points,
                                      total_coins=total_coins)
                self.create_user_pointsdetail(user_id, point, operation_type, points_status, points_type)

    def create_user_pointsdetail(self, user_id, points, operation_type, points_type, points_status, points_source=0):
        """
        创建用户积分明细
        :param user_id:用户标识
        :param points:积分
        :param operation_type:操作类型：（1：增加积分或0：减少积分）
        :param points_type:积分类型：（0：项目或1：任务）
        :param points_status:积分状态：（1：有效）
        :param points_source:积分来源：追溯积分
        :return:
        """

        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)
            PointsDetail.objects.create(user=user,
                                        operation_points=points,
                                        available_points=points,
                                        operation_type=operation_type,
                                        points_type=points_type,
                                        points_status=points_status,
                                        points_source=points_source)

    def user_total_points(self, task_id, points):
        assessment_weight = 0
        if task_id is not None:
            task = Task.objects.get(id=task_id)
            if task:
                # 取任务的评级
                if task.task_assessment:
                    task_assessment = TaskAssessment.objects.get(id=task.task_assessment.id)
                    if task_assessment:
                        assessment_weight = int(task_assessment.weight * points)

        return assessment_weight


class ProjectCostAnalysisView(APIView):
    """
    项目人员工资成本
    """

    def get(self, request, format=None):
        try:
            list_project_person_objects.clear()

            project_id = request.query_params.get('project_id', None)

            self.get_all_cost(project_id)


        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=list_project_person_objects)

    def get_all_cost(self, project_id):
        """
        计算所有成本
        """

        self.get_project_manager_cost(project_id)
        self.get_market_manager_cost(project_id)
        self.get_task_manager_cost(project_id)

    def get_project_manager_cost(self, project_id):
        """
        计算项目负责人平均工资
        """

        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project is not None:
                # 计算天数
                duration = BusinessPublic.Caltime(project.end_time, project.begin_time)
                if project.receiver:
                    receiver_id = project.receiver.id

                    user = UserProfile.objects.get(id=receiver_id)
                    if user:
                        salary = user.base_salary

                        aveage_fee = salary / 21.75
                        aveage_fee = round(aveage_fee, 2)

                        total_fee = duration * aveage_fee
                        total_fee = round(total_fee, 2)

                        salary_obj = {}
                        salary_obj["person_nums"] = 1
                        salary_obj["user"] = user.name
                        salary_obj["duration"] = duration
                        salary_obj["name"] = '平均工资'
                        salary_obj["fee"] = int(aveage_fee)
                        salary_obj["total_fee"] = int(total_fee)

                        salary_obj["project"] = {}
                        salary_obj["type"] = 0
                        salary_obj["role"] = "项目负责人"

                        list_project_person_objects.append(salary_obj)

                        return int(total_fee)

    def get_market_manager_cost(self, project_id):
        """
        计算商务人员平均工资
        """

        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project is not None:
                if project.sender:

                    duration = BusinessPublic.Caltime(project.end_time, project.begin_time)
                    sender_id = project.sender.id

                    user = UserProfile.objects.get(id=sender_id)
                    if user:
                        salary = user.base_salary

                        aveage_fee = salary / 21.75
                        aveage_fee = round(aveage_fee, 2)

                        total_fee = duration * aveage_fee
                        total_fee = round(total_fee, 2)

                        salary_obj = {}
                        salary_obj["person_nums"] = 1
                        salary_obj["user"] = user.name
                        salary_obj["duration"] = duration
                        salary_obj["name"] = '平均工资'
                        salary_obj["fee"] = int(aveage_fee)
                        salary_obj["total_fee"] = int(total_fee)

                        salary_obj["project"] = {}
                        salary_obj["type"] = 0
                        salary_obj["role"] = "商务人员"

                        list_project_person_objects.append(salary_obj)

                        return int(total_fee)

    def get_task_manager_cost(self, project_id):
        """
        计算所有任务负责人平均工资
        """

        if project_id is not None:
            duration = 0

            project = Project.objects.get(id=project_id)
            if project is not None:
                duration = BusinessPublic.Caltime(project.end_time, project.begin_time)

            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id, is_active=1)
            all_total_fee = 0
            salary = 0

            for task in tasks:
                if task:
                    if task.receiver:
                        receiver_id = task.receiver.id
                        user = UserProfile.objects.get(id=receiver_id)
                        if user:
                            salary = user.base_salary
                    else:
                        task_type = TaskType.objects.get(id=task.task_type.id)
                        salary = task_type.average_salary

                    aveage_fee = salary / 21.75
                    aveage_fee = round(aveage_fee, 2)

                    total_fee = duration * aveage_fee
                    total_fee = round(total_fee, 2)

                    salary_obj = {}
                    salary_obj["person_nums"] = 1
                    if task.receiver:
                        salary_obj["user"] = task.receiver.name
                    else:
                        salary_obj["user"] = ''
                    salary_obj["duration"] = duration
                    salary_obj["name"] = '平均工资'
                    salary_obj["fee"] = int(aveage_fee)
                    salary_obj["total_fee"] = int(total_fee)

                    salary_obj["task"] = {}
                    salary_obj["type"] = 1
                    salary_obj["role"] = "任务负责人"

                    list_project_person_objects.append(salary_obj)

                    all_total_fee = all_total_fee + int(total_fee)

            return all_total_fee


class ProjectFeeCostAnalysisView(APIView):
    """
    项目其它费用成本
    """

    def get(self, request, format=None):
        try:
            list_project_fee_objects.clear()

            project_id = request.query_params.get('project_id', None)

            self.get_projectfee_cost(project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=list_project_fee_objects)

    def get_projectfee_cost(self, project_id):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                duration = BusinessPublic.Caltime(project.end_time, project.begin_time)

                all_total_fee = 0
                tasks = Task.objects.filter(project_id=project_id, is_active=1)
                if tasks:
                    # 项目总人数 = 任务总人数 + 项目负责人 + 商务人员
                    project_person_nums = tasks.count() + 2

                    # 公司总人数
                    users = UserProfile.objects.filter(base_salary__gt=0)
                    if users:
                        company_person_nums = users.count()

                        fees = ProjectFee.objects.filter(project_id=project.id)
                        if fees:
                            for fee in fees:
                                aveage_fee = fee.value / company_person_nums
                                aveage_fee = aveage_fee / 30
                                aveage_fee = round(aveage_fee, 2)

                                total_fee = aveage_fee * project_person_nums * duration
                                total_fee = round(total_fee, 2)

                                fee_obj = {}
                                fee_obj["id"] = ''
                                fee_obj["person_nums"] = project_person_nums
                                fee_obj["duration"] = duration
                                fee_obj["name"] = fee.name
                                fee_obj["fee"] = int(aveage_fee)
                                fee_obj["total_fee"] = int(total_fee)
                                fee_obj["type"] = 1
                                list_project_fee_objects.append(fee_obj)

                                all_total_fee = all_total_fee + int(total_fee)

                return all_total_fee


class ProjectCostAnalysisFinishedView(APIView):
    """
    项目成本分析完成
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id', None)
            # 项目总积分
            project_points = request.data.get('project_points', None)

            self.update_project(project_id, project_points)
            self.update_task(project_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, project_points):
        if project_id is not None and project_points is not None:
            project = Project.objects.get(id=project_id)
            project.points = project_points
            project.save()

    def update_task(self, project_id):
        if project_id is not None:
            projectpoints = ProjectPoints.objects.filter(project_id=project_id, type=1)
            if projectpoints:
                for projectpoint in projectpoints:
                    if projectpoint:
                        if projectpoint.task:
                            task = Task.objects.get(id=projectpoint.task.id)
                            task.points = projectpoint.points
                            task.save()


class ProjectPublishView(APIView):
    """项目发布"""


class HasProjectView(APIView):
    """
    是否存在项目
    """

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        projects = Project.objects.filter(sender_id=user_id)
        if len(projects) > 0:
            return MykeyResponse(status=status.HTTP_200_OK, data=1, msg='请求成功')
        return MykeyResponse(status=status.HTTP_200_OK, data=0, msg='请求成功')


class ProjectHasTaskView(APIView):
    """
    项目是否存在任务
    """

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        project_id = request.query_params.get('project_id', None)
        tasks = Task.objects.filter(project_id=project_id, sender_id=user_id)
        if len(tasks) > 0:
            return MykeyResponse(status=status.HTTP_200_OK, data=1, msg='请求成功')
        return MykeyResponse(status=status.HTTP_200_OK, data=0, msg='请求成功')
