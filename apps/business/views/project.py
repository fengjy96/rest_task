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
    ProjectSerializer, ProjectRejectReasonSerializer, ProjectFeeSerializer, ProjectReceiverListSerializer, ProjectCreateSerializer
)
from business.views.base import BusinessPublic
from business.filters import ProjectFilter
from rbac.models import UserProfile
from configuration.models import Salary


class ProjectViewSet(ModelViewSet):
    """
    项目：增删改查
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CommonPagination
    # 局部定制过滤器
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 对指定的字段进行搜索
    search_fields = ('name',)
    # 对指定的字段进行过滤
    filter_fields = ('receiver_id', 'is_active', 'customer', 'style')
    # 对指定的字段进行排序：使用 ordering_fields 属性明确指定可以对哪些字段执行排序，
    # 这有助于防止意外的数据泄露
    ordering_fields = ('id',)
    # 指定筛选类
    filter_class = ProjectFilter
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'create':
            return ProjectCreateSerializer
        elif self.action == 'list':
            return ProjectSerializer
        return ProjectSerializer

    def create(self, request, *args, **kwargs):
        # 项目创建人
        request.data['sender'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # 项目状态为激活
        is_active = 1

        return Project.objects.filter(is_active=is_active)


class ProjectReceiverListView(ListAPIView):
    """
    选择项目负责人
    """

    queryset = UserProfile.objects.filter(roles__id=7)
    serializer_class = ProjectReceiverListSerializer


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

            self.update_project(project_id, points, request=request)
            self.update_task(project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, points, request):
        """
        更新项目表信息
        """
        if project_id is not None:
            from business.models.project import Project
            project = Project.objects.get(id=project_id)
            if project is not None:
                # 已审核
                project.audit_status = 2
                # 等待项目负责人接手项目
                project.receive_status = 2
                # 项目积分
                project.points = points
                project.save()

                BusinessPublic.create_message(project.auditor_id, project.sender_id,
                                              '你有新的项目等待接手!')
                BusinessPublic.create_message(project.auditor_id, project.receiver_id,
                                              '项目已通过审核!')

    def update_task(self, project_id, ):
        """
        更新任务表信息
        """
        if project_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    # 等待项目负责人接手项目
                    task.send_status = 2
                    if task.receiver_id:
                        # 等待任务负责人接手任务
                        task.receive_status = 2
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
                step.send_status = 2
                if step.receiver_id is not None:
                    step.receive_status = 2
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
            reason = request.data.get('reason')

            self.update_project(project_id, reason)
            self.update_task(project_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_project(self, project_id, reason):
        if project_id is not None:
            # from business.models.project import Project
            project = Project.objects.get(id=project_id)
            if project is not None:
                # 驳回
                project.audit_status = 3
                project.save()

                BusinessPublic.create_reason(project.id, project.sender_id, project.receiver_id,
                                             'ProjectRejectReason', reason)
                BusinessPublic.create_message(project.sender_id, project.receiver_id,
                                              '你的项目已被驳回，请尽快处理!')

    def update_task(self, project_id):
        if project_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    # 驳回
                    task.audit_status = 3
                    task.save()


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
                project.receive_status = 3
                project.save()
                BusinessPublic.create_message(project.receiver_id, project.auditor_id,
                                              '项目负责人已接手，项目正式开始!')
                self.update_task(project_id)

    def update_task(self, project_id):
        if project_id is not None:
            from business.models.task import Task
            tasks = Task.objects.filter(project_id=project_id)
            for task in tasks:
                if task is not None:
                    # 项目负责人已接手,项目正式开始
                    task.send_status = 3
                    if task.receiver_id is not None:
                        task.save()

                        BusinessPublic.create_message(task.sender_id, task.receiver_id,
                                                      '你有新的任务等待接手!')
                        self.update_step(task.id)

    def update_step(self, task_id):
        if task_id is not None:
            from business.models.step import Step
            steps = Step.objects.filter(task_id=task_id)
            for step in steps:
                # 项目负责人已接手, 项目正式开始
                step.send_status = 3
                step.save()


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
