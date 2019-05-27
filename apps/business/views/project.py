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
from business.models.project import Project, ProjectFee, ProjectRejectReason, ProjectCost
from business.serializers.project_serializer import (
    ProjectListSerializer, ProjectRejectReasonSerializer, ProjectFeeSerializer, ProjectReceiverListSerializer,
    ProjectSerializer,
    ProjectAuditorListSerializer)
from business.views.base import BusinessPublic
from business.filters import ProjectFilter
from rbac.models import UserProfile
from configuration.models import Salary, ProjectStatus, TaskStatus


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
            sender_id = request.data.get('sender_id')

            if project_id is not None and auditor_id is not None and sender_id is not None:
                self.update_project(project_id, auditor_id)
                self.update_task(project_id, auditor_id, sender_id)

                BusinessPublic.create_message(sender_id, auditor_id, menu_id=2, messages='有新的项目需要你的审核，请尽快处理!')

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
            if project is not None:
                project.auditor_id = auditor_id
                # 审核中
                project.audit_status = 1
                project.save()

    def update_task(self, project_id, auditor_id, sender_id):
        """
        更新任务审核信息
        """
        if sender_id is not None and auditor_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    task.auditor_id = auditor_id
                    task.save()


class ProjectAuditPassView(APIView):
    """
    商务人员项目审核通过
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')
            # 项目积分
            points = request.data.get('points')

            # 更新项目
            self.update_project(project_id, points)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, points):
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
                project.receive_status = ProjectStatus.objects.get(key='wait_accept')
                # 项目积分
                project.points = points
                project.save()

                BusinessPublic.create_message(project.auditor_id, project.sender_id, menu_id=2,
                                              messages='你有新的项目等待接手!')
                BusinessPublic.create_message(project.auditor_id, project.receiver_id, menu_id=2,
                                              messages='项目已通过审核!')

                # 更新任务
                self.update_task(project_id)

    def update_task(self, project_id):
        """
        更新任务表信息
        """
        if project_id is not None:
            # 获取项目负责人 id
            project = Project.objects.get(id=project_id)

            # 根据项目 id 过滤所有任务
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)

            for task in tasks:
                if task is not None:
                    # 如果任务不存在任务审核员，则将项目负责人作为任务审核员
                    if task.auditor_id is not None:
                        task.auditor_id = project.receiver_id
                    if task.receiver_id is not None:
                        # 等待任务负责人接手任务
                        task.receive_status = TaskStatus.objects.get(key='wait_accept')
                        task.save()

                        self.update_step(task.id)

    def update_step(self, task_id):
        """
        更新步骤表信息
        """
        if task_id is not None:
            from business.models.step import Step
            steps = Step.objects.filter(task_id=task_id)
            for step in steps:
                if step.receiver_id is not None:
                    # step.receive_status = 2
                    step.save()


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

                BusinessPublic.create_reason(project.id, project.auditor_id, project.sender_id,
                                             'ProjectRejectReason', reason)
                BusinessPublic.create_message(project.auditor_id, project.sender_id, menu_id=2,
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
                project.receive_status = ProjectStatus.objects.get(key='accepted')
                project.save()
                BusinessPublic.create_message(project.receiver_id, project.auditor_id, menu_id=2,
                                              messages='项目负责人已接手，项目正式开始!')
                self.update_task(project_id)

    def update_task(self, project_id):
        if project_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    # 项目负责人已接手，项目正式开始
                    task.receive_status = TaskStatus.objects.get(key='wait_accept')
                    if task.receiver_id is not None:
                        task.save()

                        BusinessPublic.create_message(task.sender_id, task.receiver_id, menu_id=2,
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
                project.receive_status = ProjectStatus.objects.get(key='rejected')
                project.save()

                BusinessPublic.create_reason(project.id, project.receiver_id, project.auditor_id,
                                             'ProjectRejectReason', reason)
                BusinessPublic.create_message(project.receiver_id, project.auditor_id, menu_id=2,
                                              messages='你的项目已被驳回，请尽快处理!')



class ProjectCostAnalysisView(APIView):
    """
    6.分析项目成本
    """

    def post(self, request, format=None):
        try:
            project_id = request.data.get('project_id')

            self.update_projectcost(project_id)
            self.update_taskcost(project_id)
            self.update_projectfee_cost(project_id)

            queryset = ProjectCost.objects.filter(project_id=project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    # 计算项目负责人平均工资
    def update_projectcost(self, project_id):
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            if project is not None:
                # duration = project.duration
                duration = 12
                receiver_id = project.receiver_id

                user_salary = Salary.objects.get(user_id=receiver_id)
                salary = user_salary.salary

                aveage_fee = salary / 21.75
                aveage_fee = round(aveage_fee, 2)

                total_fee = duration * aveage_fee
                total_fee = round(total_fee, 2)

                # self.create_cost(project.id, '', project.receiver_id, 1, project.duration,
                #                  '平均工资', aveage_fee, total_fee)
                self.create_cost(project.id, '', project.receiver_id, 1, 12,
                                 '平均工资', aveage_fee, total_fee)

    # 计算所有任务负责人平均工资
    def update_taskcost(self, project_id):
        if project_id is not None:
            duration = 0

            project = Project.objects.get(id=project_id)
            if project is not None:
                duration = 12
                # duration = project.duration

            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    receiver_id = tasks.receiver_id

                    user_salary = Salary.objects.get(user_id=receiver_id)
                    salary = user_salary.salary

                    aveage_fee = salary / 21.75
                    aveage_fee = round(aveage_fee, 2)

                    total_fee = duration * aveage_fee
                    total_fee = round(total_fee, 2)

                    self.create_cost(task.id, '', task.receiver_id, 1, duration,
                                     '平均工资', aveage_fee, total_fee)

    # 计算费用表中的费用分摊
    def update_projectfee_cost(self, project_id):
        if project_id is not None:

            project = Project.objects.get(id=project_id)
            if project is not None:
                duration = 12
                # duration = project.duration

                from business.models.task import Task
                tasks = Task.objects.filter(project_id=project_id)

                # 项目总人数 = 任务总人数 + 项目负责人
                project_person_nums = tasks.count() + 1

                # 公司总人数
                users = UserProfile.objects.filter(company_id=project.company_id)
                company_person_nums = users.count()

                for task in tasks:
                    if task is not None:
                        receiver_id = tasks.receiver_id

                        fees = ProjectFee.objects.get(project_id=project.id)
                        fee = fees.value

                        aveage_fee = fee / company_person_nums
                        aveage_fee = aveage_fee / 30
                        aveage_fee = round(aveage_fee, 2)

                        total_fee = aveage_fee * project_person_nums * duration
                        total_fee = round(total_fee, 2)

                        self.create_cost('', '', '', project_person_nums, duration, fees.name, aveage_fee,
                                         total_fee)

    def create_cost(self, task_id, task_type_id, user_id, person_nums, duration, name, fee, total_fee):
        """
        创建成本
        """
        project_cost = ProjectCost(
            task_id=task_id,
            task_type_id=task_type_id,
            user_id=user_id,
            person_nums=person_nums,
            duration=duration,
            name=name,
            fee=fee,
            total_fee=total_fee
        )

        project_cost.save()
