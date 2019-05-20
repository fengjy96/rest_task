from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import CommonPagination
from rbac.models import UserProfile
from business.models.task import Task, TaskAllocateReason
from business.serializers.task_serializer import TaskSerializer, TaskListSerializer, TaskAllocateReasonSerializer, \
    TaskCreateSerializer
from utils.basic import MykeyResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import TaskFilter
from business.views.base import BusinessPublic
from business.models.project import Project
from business.models.files import Files


class TaskReceiverView(APIView):
    """
    获取任务负责人
    """

    def get(self, request, format=None):
        # 设计方式
        # task_type_id = request.data.get('task_type_id')

        users = UserProfile.objects.filter(roles__id=6)

        list_objects = []

        for user in users:
            tasks = Task.objects.filter(receiver_id=user.id)

            if len(tasks) > 0:
                for task in tasks:
                    if task is not None:
                        dict_obj1 = {}
                        dict_obj1["user_id"] = user.id
                        dict_obj1["name"] = user.name
                        dict_obj1["task_type"] = task.task_type.name
                        dict_obj1["task_progress"] = task.progress
                        dict_obj1["end_time"] = task.end_time
                        dict_obj1["leftdays"] = 12
                        # dict_obj1["leftdays"] = task.duration
                        dict_obj1["receive_status"] = task.receive_status
                        list_objects.append(dict_obj1)
            else:
                dict_obj2 = {}
                dict_obj2["user_id"] = user.id
                dict_obj2["name"] = user.name
                dict_obj2["task_type"] = ""
                dict_obj2["task_progress"] = ""
                dict_obj2["end_time"] = ""
                dict_obj2["leftdays"] = 0
                dict_obj2["receive_status"] = 0
                list_objects.append(dict_obj2)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=list_objects)


class TaskViewSet(ModelViewSet):
    """
    任务：增删改查
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('id',)
    # 指定筛选类
    filter_class = TaskFilter
    # 指定分页类
    pagination_class = CommonPagination
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'list':
            return TaskListSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        # 项目创建人
        request.data['sender'] = request.user.id
        if request.data['receiver']:
            request.data['receive_status'] = 1
        else:
            request.data['receive_status'] = 0
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if request.data['receiver']:
            request.data['receive_status'] = 1
        else:
            request.data['receive_status'] = 0
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


class TaskListView(APIView):
    """
    任务：增删改查
    """
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = TaskFilter
    ordering_fields = ('id',)

    def get_queryset(self, request):
        is_active = 0
        audit_status = 0
        receive_status = 0
        is_finished = 0
        send_status = 0

        # 前端逻辑判断
        accept_status = request.data.get('accept_status')

        if accept_status is not None:
            # 任务为激活状态
            is_active = 1
            # 项目负责人已接手,项目正式开始
            send_status = 3

            # 任务未开始
            if accept_status == 0:
                # 等待任务负责人接手任务
                audit_status = 0
                receive_status = 2
                is_finished = 0
            # 任务进行中
            elif accept_status == 1:
                # 任务负责人已接手,任务执行中
                audit_status = 0
                receive_status = 3
                is_finished = 0
            # 任务已完成
            elif accept_status == 2:
                # 任务负责人已接手,任务执行中
                audit_status = 0
                receive_status = 3
                is_finished = 1
            # 任务未审核
            elif accept_status == 3:
                audit_status = 1
                receive_status = 3
                is_finished = 0
            # 任务已审核
            elif accept_status == 4:
                audit_status = 2
                receive_status = 3
                is_finished = 1

        return Task.objects.filter(is_active=is_active, send_status=send_status, receive_status=receive_status,
                                   audit_status=audit_status, is_finished=is_finished)


class TaskFileisEmptyViewSet(ModelViewSet):
    """
    判断参考文件是否存在为空
    """

    def get(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')
            if project_id is not None:
                project = Project.objects.get(id=project_id)
                if project is not None:
                    tasks = Task.objects.filter(project_id=project_id)
                    if tasks is not None:
                        for task in tasks:
                            if task is not None:
                                files = Files.objects.filter(task_id=task.id)
                                if files is not None:
                                    if files.count() == 0:
                                        return MykeyResponse(status=status.HTTP_400_BAD_REQUEST,
                                                             msg=task.name + '的参考文件为空')
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')


class TaskAllocateReasonViewSet(ModelViewSet):
    """
    任务分派原因：增删改查
    """
    queryset = TaskAllocateReason.objects.all()
    serializer_class = TaskAllocateReasonSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('task_id', 'receiver_id')
    ordering_fields = ('id',)
    # permission_classes = [IsAuthenticated]


class TaskAcceptView(APIView):
    """
    接手任务
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id')
            # 任务设计类型标识
            task_design_type_id = request.data.get('task_design_type_id')

            self.update_task(task_id)
            self.update_step(task_id, task_design_type_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 任务负责人已接手,任务执行中
                task.receive_status = 3
                task.save()
                BusinessPublic.create_message(task.receiver_id, task.sender_id,
                                              '任务负责人已接手,任务执行中!')

    def update_step(self, task_id, task_design_type_id):
        if task_id is not None:
            from business.models.step import Step
            steps = Step.objects.filter(task_id=task_id, task_design_type_id=task_design_type_id)
            for step in steps:
                step.receive_status = 3
                status.is_active = 1
                step.save()


class TaskAuditSubmitView(APIView):
    """
    任务提交审核
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id')

            self.update_task(task_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 审核中
                task.audit_status = 1
                task.save()
                BusinessPublic.create_message(task.receiver_id, task.sender_id,
                                              '有新的任务需要你的审核，请尽快处理!')


class TaskAuditSuccessView(APIView):
    """
    任务审核通过
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id')

            self.update_task(task_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 审核通过
                task.audit_status = 2
                # 任务已完成
                task.is_finished = 1
                task.save()
                BusinessPublic.create_message(task.receiver_id, task.sender_id,
                                              '任务已通过审核!')


class TaskAllocateView(APIView):
    """
    任务转派
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id')
            # 接收者标识
            receiver_id = request.data.get('receiver_id')
            # 转派原因
            reason = request.data.get('reason')

            self.update_task(task_id, receiver_id, reason)
            self.update_step(task_id, receiver_id)


        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id, receiver_id, reason):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                task.receiver = receiver_id
                task.receive_status = 2
                task.save()

                BusinessPublic.create_reason(task_id, task.sender_id, task.receiver_id,
                                             'TaskAllocateReason', reason)
                BusinessPublic.create_message(task.receiver_id, task.sender_id,
                                              '已安排新的任务,请查看!')
                self.update_step(task.id, task.sender_id)

    def update_step(self, task_id, receiver_id):
        if task_id is not None:
            from business.models.step import Step
            steps = Step.objects.filter(task_id=task_id)
            for step in steps:
                step.receiver = receiver_id
                step.receive_status = 2
                step.save()
