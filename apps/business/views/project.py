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
from configuration.models import ProjectStatus, TaskStatus, ReasonType

# 项目成本
list_project_person_objects = []


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
        # 如果存在项目负责人，则将项目接收状态置为 '已指派项目负责人'
        if request.data.get('receiver') is not None:
            request.data['receive_status'] = ProjectStatus.objects.get(key='assigned').id
        # 如果不存在项目负责人，则将项目接手状态置为 '未指派项目负责人'
        else:
            request.data['receive_status'] = ProjectStatus.objects.get(key='unassigned').id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

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
                queryset_project_manager = queryset.filter(receiver_id=user_id, audit_status=2)
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
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('wait_accept')
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
                BusinessPublic.create_message(project.receiver_id, project.auditor_id, menu_id=2,
                                              messages='项目负责人已接手，项目正式开始!')
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
                # 拒接
                project.receive_status = BusinessPublic.GetProjectStatusObjectByKey('rejected')
                project.save()

                BusinessPublic.create_reason(project.id, project.receiver.id, project.auditor.id,
                                             BusinessPublic.GetReasonTypeIdByKey('project_reject'),
                                             reason)
                BusinessPublic.create_message(project.receiver.id, project.auditor.id, menu_id=2,
                                              messages='你的项目已被驳回，请尽快处理!')


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

                BusinessPublic.create_message(project.auditor_id, project.receiver_id, menu_id=2,
                                              messages='恭喜,你的项目已验收通过!')


class ProjectCostAnalysisView(APIView):
    """
    分析项目人员成本
    """
    def get(self, request, format=None):
        try:
            list_project_person_objects.clear()

            project_id = request.data.get('project_id')

            self.get_project_manager_cost(project_id)
            self.get_market_manager_cost(project_id)
            self.get_task_manager_cost(project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败',data=list_project_person_objects)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功',data=list_project_person_objects)

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
                        salary_obj["project"] = self.get_project_objects(project.id)
                        salary_obj["type"] = 0
                        salary_obj["role"] = "项目负责人"
                        salary_obj["person_nums"] = 1
                        salary_obj["user"] = user.name
                        salary_obj["duration"] = duration
                        salary_obj["name"] = '平均工资'
                        salary_obj["fee"] = aveage_fee
                        salary_obj["total_fee"] = total_fee

                        list_project_person_objects.append(salary_obj)

    def get_market_manager_cost(self, project_id):
        """
        计算商务人员平均工资
        """
        list_objects = []
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
                        salary_obj["project"] = self.get_project_objects(project.id)
                        salary_obj["type"] = 0
                        salary_obj["role"] = "商务人员"
                        salary_obj["person_nums"] = 1
                        salary_obj["user"] = user.name
                        salary_obj["duration"] = duration
                        salary_obj["name"] = '平均工资'
                        salary_obj["fee"] = aveage_fee
                        salary_obj["total_fee"] = total_fee

                        list_project_person_objects.append(salary_obj)

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
            for task in tasks:
                if task:
                    if task.receiver:
                        receiver_id = task.receiver.id

                        user = UserProfile.objects.get(id=receiver_id)
                        if user:
                            salary = user.base_salary

                            aveage_fee = salary / 21.75
                            aveage_fee = round(aveage_fee, 2)

                            total_fee = duration * aveage_fee
                            total_fee = round(total_fee, 2)

                            salary_obj = {}
                            salary_obj["task"] = self.get_task_objects(task.id)
                            salary_obj["type"] = 1
                            salary_obj["role"] = "任务负责人"
                            salary_obj["person_nums"] = 1
                            salary_obj["user"] = project.receiver.name
                            salary_obj["duration"] = project.duration
                            salary_obj["name"] = '平均工资'
                            salary_obj["fee"] = aveage_fee
                            salary_obj["total_fee"] = total_fee

                            list_project_person_objects.append(salary_obj)

    def get_project_objects(self,id):
        """
        项目信息
        """
        project_objects_data = []

        project = Project.objects.get(id=id)
        if project:
            dict_obj = {}
            dict_obj["id"] = project.id
            dict_obj["name"] = project.name
            dict_obj["style"] = project.style
            dict_obj["customer"] = project.customer

            if project.sender:
                dict_obj["sender"] = project.sender.name
            else:
                dict_obj["sender"] = ''
            if project.receiver:
                dict_obj["receiver"] = project.receiver.name
            else:
                dict_obj["receiver"] = ''
            if project.auditor:
                dict_obj["auditor"] = project.auditor.name
            else:
                dict_obj["auditor"] = ''

            dict_obj["audit_status"] = project.audit_status
            dict_obj["receive_status"] = project.receive_status
            dict_obj["duration"] = BusinessPublic.Caltime(project.end_time, project.begin_time)
            dict_obj["begin_time"] = project.begin_time
            dict_obj["end_time"] = project.end_time
            dict_obj["add_time"] = project.add_time
            dict_obj["points"] = project.points
            dict_obj["progress"] = project.progress

            project_objects_data.append(dict_obj)

        return project_objects_data

    def get_task_objects(self,id):
        """
        项目信息
        """
        task_objects_data = []

        task = Task.objects.get(id=id)
        if task:
            dict_obj = {}
            dict_obj["id"] = task.id
            dict_obj["name"] = task.name
            dict_obj["task_type"] = task.task_type.name
            dict_obj["content"] = task.content
            dict_obj["task_priority"] = task.task_priority.name
            dict_obj["task_quality"] = task.task_quality.name
            dict_obj["begin_time"] = task.begin_time
            dict_obj["end_time"] = task.end_time
            dict_obj["duration"] = BusinessPublic.Caltime(task.end_time, task.begin_time)
            dict_obj["points"] = task.points
            dict_obj["memo"] = task.memo
            dict_obj["project"] = task.project.name

            if task.sender:
                dict_obj["sender"] = task.sender.name
            else:
                dict_obj["sender"] = ''

            if task.receiver:
                dict_obj["receiver"] = task.receiver.name
            else:
                dict_obj["receiver"] = ''

            if task.auditor:
                dict_obj["auditor"] = task.auditor.name
            else:
                dict_obj["auditor"] = ''

            dict_obj["send_status"] = task.send_status
            dict_obj["receive_status"] = task.receive_status
            dict_obj["audit_status"] = task.audit_status
            dict_obj["is_active"] = task.is_active
            dict_obj["is_finished"] = task.is_finished
            dict_obj["add_time"] = task.add_time
            dict_obj["progress"] = task.progress

            task_objects_data.append(dict_obj)

        return task_objects_data

    def get_user_objects(self,id):
        """
        项目信息
        """
        user_objects_data = []

        user = UserProfile.objects.get(id=id)
        if user:
            dict_obj = {}
            dict_obj["id"] = user.id
            dict_obj["name"] = user.name

            user_objects_data.append(dict_obj)

        return user_objects_data


class ProjectFeeCostAnalysisView(APIView):
    """
    分析项目费用分摊
    """
    def get(self, request, format=None):
        try:
            project_id = request.data.get('project_id')

            list_project_fee_objects = self.get_projectfee_cost(project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功',data=list_project_fee_objects)

    def get_projectfee_cost(self, project_id):
        list_project_fee_objects = []

        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project:
                duration = BusinessPublic.Caltime(project.end_time,project.begin_time)

                tasks = Task.objects.filter(project_id=project_id)
                if tasks is not None:
                    # 项目总人数 = 任务总人数 + 项目负责人
                    project_person_nums = tasks.count() + 1

                    # 公司总人数
                    #users = UserProfile.objects.filter(company_id=project.company_id)
                    users = UserProfile.objects.all()
                    if users:
                        company_person_nums = users.count()

                        fees = ProjectFee.objects.filter(project_id=project.id)
                        for fee in fees:
                             aveage_fee = fee.value / company_person_nums
                             aveage_fee = aveage_fee / 30
                             aveage_fee = round(aveage_fee, 2)

                             total_fee = aveage_fee * project_person_nums * duration
                             total_fee = round(total_fee, 2)

                             fee_obj = {}
                             fee_obj["id"] = ""
                             fee_obj["person_nums"] = project_person_nums
                             #fee_obj["user"] = ""
                             fee_obj["duration"] = duration
                             fee_obj["name"] = fee.name
                             fee_obj["fee"] = aveage_fee
                             fee_obj["total_fee"] = total_fee

                             list_project_fee_objects.append(fee_obj)

        return list_project_fee_objects


class ProjectCostAnalysisFinishedView(APIView):
    """
    项目成本分析完成
    """
    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id')
            self.update_task(project_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, project_id):
        if project_id is not None:
            projectpoints = ProjectPoints.objects.filter(project_id=project_id)
            if projectpoints:
                for projectpoint in projectpoints:
                    if projectpoint:
                        if projectpoint.task:
                            task = Task.objects.get(id=projectpoint.task.id)
                            task.points = projectpoint.points
                            task.save()