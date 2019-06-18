from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import CommonPagination
from utils.basic import MykeyResponse
from business.models.project import Project, ProjectFee, ProjectRejectReason
from business.serializers.project_serializer import (
    ProjectListSerializer, ProjectRejectReasonSerializer, ProjectFeeSerializer, ProjectReceiverListSerializer,
    ProjectSerializer,
    ProjectAuditorListSerializer)
from business.views.base import BusinessPublic
from business.filters import ProjectFilter
from rbac.models import UserProfile
from business.models.task import Task
from points.models.projectpoints import ProjectPoints
from points.models.points import Points
from points.models.pointsdetail import PointsDetail
from configuration.models.project_conf import ProjectStatus, Fee
from configuration.models.task_conf import TaskType, TaskAssessment

# 项目人员成本
list_project_person_objects = []
# 项目费用成本
list_project_fee_objects = []

class ProjectViewSet(ModelViewSet):
    """
    项目：增删改查
    """

    # 获取查询集
    queryset = Project.objects.all()
    # 指定分页类
    pagination_class = CommonPagination
    # 指定过滤 backends
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 指定搜索字段
    search_fields = ('name',)
    # 对指定的字段进行排序：使用 ordering_fields 属性明确指定可以对哪些字段执行排序，
    # 这有助于防止意外的数据泄露
    ordering_fields = ('id',)
    # 指定筛选类
    filter_class = ProjectFilter
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def create(self, request, *args, **kwargs):
        # 将当前登录用户作为项目创建人
        request.data['sender'] = request.user.id
        receiver_id = request.data.get('receiver', None)
        # 如果存在项目负责人，则将项目接收状态置为 '已指派项目负责人'
        if receiver_id is not None:
            BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2,
                                          messages='你有新的项目等待接手!')
            request.data['receive_status'] = ProjectStatus.objects.get(key='wait_accept').id
        # 如果不存在项目负责人，则将项目接手状态置为 '未指派项目负责人'
        else:
            request.data['receive_status'] = ProjectStatus.objects.get(key='unassigned').id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):

        project_id = request.data.get('id', None)
        receiver_id = request.data.get('receiver', None)
        if receiver_id is not None:
            if project_id is not None:
                project = Project.objects.get(id=project_id)
                if receiver_id != project.receiver.id:
                    # 更新任务表的项目负责人
                    Task.objects.filter(project_id=project_id).update(sender_id=receiver_id)
                    # 更新任务表的上级主管
                    Task.objects.filter(project_id=project_id, superior=project.receiver.id).update(superior=receiver_id)
                    # 更新项目积分表
                    ProjectPoints.objects.filter(user_id=project.receiver.id, is_create=0, project_id=project_id).update(user_id=receiver_id)
                    # 新增消息
                    BusinessPublic.create_message(request.user.id, receiver_id, menu_id=2,
                                              messages='你有新的项目等待接手!')
            request.data['receive_status'] = ProjectStatus.objects.get(key='wait_accept').id
        else:
            request.data['receive_status'] = ProjectStatus.objects.get(key='unassigned').id

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-add_time')

        queryset = self.filter_list_queryset(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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


class ProjectReceiverListView(ListAPIView):
    """
    选择项目负责人
    """

    queryset = UserProfile.objects.filter(roles__id=7)
    serializer_class = ProjectReceiverListSerializer

    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectAuditorListView(ListAPIView):
    """
    获取所有项目审核员
    """

    queryset = UserProfile.objects.filter(roles__id=5)
    serializer_class = ProjectAuditorListSerializer

    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectFeeViewSet(ModelViewSet):
    """
    项目费用：增删改查
    """
    queryset = ProjectFee.objects.all()
    serializer_class = ProjectFeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('project_id',)
    ordering_fields = ('id',)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        project_id = request.query_params.get('project_id', None)
        is_first = request.query_params.get('is_first', None)
        if is_first == 'true':
            self.create_project_fee(project_id)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create_project_fee(self, project_id):
        if project_id is not None:
            fees = Fee.objects.all()
            if fees:
                for fee in fees:
                      if fee:
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
    filter_fields = ('project_id',)
    permission_classes = (IsAuthenticated,)


class ProjectAuditSubmitView(APIView):
    """
    商务人员项目审核提交
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')
            # 审核员标识
            auditor_id = request.data.get('auditor_id')
            # 发送者标识
            #sender_id = request.data.get('sender_id')

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
        if project_id is not None and auditor_id is not None:
            from business.models.project import Project
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
            # 项目标识
            project_id = request.data.get('project_id')
            # 项目积分
            #points = request.data.get('points')

            # 更新项目
            self.update_project(project_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id):
        """
        更新项目表信息
        """
        if project_id is not None:
            from business.models.project import Project
            project = Project.objects.get(id=project_id)
            if project is not None:
                if project.receiver is None:
                    raise Exception('未填写项目负责人!')
                # 已审核
                project.audit_status = 2
                # 等待项目负责人接手项目
                # project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('wait_accept')
                # 项目积分
                # project.points = points
                project.save()

                BusinessPublic.create_message(project.auditor.id, project.sender.id, menu_id=2,
                                              messages='你有新的项目等待接手!')
                BusinessPublic.create_message(project.auditor.id, project.receiver.id, menu_id=2,
                                              messages='项目已通过审核!')


class ProjectAuditRejectView(APIView):
    """
    商务人员项目审核驳回
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')
            # 驳回原因
            reason = request.data.get('reason') or ''

            self.update_project(project_id, reason)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project is not None:
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
            project_id = request.data.get('project_id')
            self.update_project(project_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id):
        if project_id is not None:
            from business.models.project import Project
            project = Project.objects.get(id=project_id)
            if project is not None:
                # 项目负责人已接手,项目正式开始
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('accepted')
                project.save()
                BusinessPublic.create_message(project.receiver_id, project.sender_id, menu_id=2,
                                              messages='项目负责人已接手!')
                self.update_task(project_id)

    def update_task(self, project_id):
        if project_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task:
                    # 项目负责人已接手，项目正式开始
                    task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_accept')
                    if task.receiver.id is not None:
                        task.save()

                        BusinessPublic.create_message(task.sender_id, task.receiver.id, menu_id=2,
                                                      messages='你有新的任务等待接手!')


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

            self.update_project(project_id, reason)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        if project_id is not None:
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

                # 积分及米值分配
                projectpoints = ProjectPoints.objects.filter(project_id=project_id, is_created = 0)
                if projectpoints:
                    for projectpoint in projectpoints:
                         if projectpoint:
                             if projectpoint.task:
                                 self.create_user_points(projectpoint.project.id, projectpoint.task.id, projectpoint.user.id, projectpoint.points, 1, 1,
                                                         projectpoint.type, projectpoint.task.task_assessment.id)
                             else:
                                 self.create_user_points(projectpoint.project.id, None, projectpoint.user.id, projectpoint.points, 1, 1,
                                                         projectpoint.type)

                             project_points = ProjectPoints.objects.get(id=projectpoint.id)
                             project_points.is_created = 1
                             project_points.save()

                BusinessPublic.create_message(project.auditor_id, project.receiver_id, menu_id=2,
                                              messages='恭喜,你的项目已验收通过!')

    def create_user_points(self, project_id, task_id, user_id, point, operation_type, points_status, points_type, task_assessment_id=None):
        """
        创建或更新用户积分以及米值,如果用户积分表中存在记录则更新,如果没有则新增
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
                total_coins = round(total_points / 1000,3)
                user_total_coins = round(user_point.total_coins,3)
                user_point.total_coins = user_total_coins + total_coins
                user_point.save()

                self.create_user_pointsdetail(user_id,total_points,operation_type,points_status,points_type)
            else:
                Points.objects.create(user=user, total_points=total_points,available_points=available_points, total_coins=total_coins)
                self.create_user_pointsdetail(user_id,point,operation_type,points_status,points_type)

    def create_user_pointsdetail(self, user_id, points,operation_type, points_type, points_status, points_source=0):
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
        if  task_id is not None:
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
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功',data=list_project_person_objects)

    def get_all_cost(self,project_id):
        """
        计算所有成本
        """

        project_manager_cost = self.get_project_manager_cost(project_id)
        market_manager_cost = self.get_market_manager_cost(project_id)
        task_manager_cost = self.get_task_manager_cost(project_id)
        total_cost = project_manager_cost + market_manager_cost + task_manager_cost

        total_obj = {}
        total_obj["person_nums"] = ''
        total_obj["user"] = ''
        total_obj["duration"] = ''
        total_obj["name"] = '合计'
        total_obj["fee"] = ''
        total_obj["total_fee"] = int(total_cost)
        total_obj["task"] = {}
        total_obj["type"] = 2
        total_obj["role"] = ''

        list_project_person_objects.append(total_obj)

    def get_project_manager_cost(self, project_id):
        """
        计算项目负责人平均工资
        """

        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project is not None:
                #计算天数
                duration = BusinessPublic.Caltime(project.end_time,project.begin_time)
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

                    duration = BusinessPublic.Caltime(project.end_time,project.begin_time)
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
                duration = BusinessPublic.Caltime(project.end_time,project.begin_time)

            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id,is_active=1)
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
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功',data=list_project_fee_objects)

    def get_projectfee_cost(self, project_id):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                duration = BusinessPublic.Caltime(project.end_time,project.begin_time)

                all_total_fee = 0
                tasks = Task.objects.filter(project_id=project_id, is_active = 1)
                if tasks:
                    # 项目总人数 = 任务总人数 + 项目负责人 + 商务人员
                    project_person_nums = tasks.count() + 2

                    # 公司总人数
                    users = UserProfile.objects.all()
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

                        total_fee_obj = {}
                        total_fee_obj["id"] = ''
                        total_fee_obj["person_nums"] = ''
                        total_fee_obj["duration"] = ''
                        total_fee_obj["name"] = '合计'
                        total_fee_obj["fee"] = ''
                        total_fee_obj["total_fee"] = all_total_fee
                        total_fee_obj["type"] = 2
                        list_project_fee_objects.append(total_fee_obj)

                return all_total_fee


class ProjectCostAnalysisFinishedView(APIView):
    """
    项目成本分析完成
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id', None)

            self.update_task(project_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')


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
