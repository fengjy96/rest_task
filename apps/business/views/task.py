from django.db.models import Q
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
        # 任务创建人
        request.data['sender'] = request.user.id
        # 获取该任务所属的项目 id
        project_id = request.data.get('project', None)
        if project_id is not None:
            # 根据项目 id 查项目负责人
            project = Project.objects.get(id=project_id)
            project_receiver_id = project.receiver_id

            # 如果存在项目负责人则将该项目负责人作为任务审核员
            if project_receiver_id is not None:
                request.data['auditor'] = project_receiver_id

        # 如果创建任务时指定了任务负责人，则任务接收状态为: 已安排任务负责人
        if request.data.get('receiver', None):
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('assigned')
        # 如果创建任务时未指定任务负责人，则任务接收状态为: 未安排任务负责人
        else:
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('unassigned')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if request.data.get('receiver', None):
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('assigned')
        else:
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('unassigned')
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
            # tasks = Task.objects.filter(receiver_id=user.id, is_active=1, receive_status__lte=3)
            tasks = Task.objects.filter(~Q(receive_status=BusinessPublic.GetTaskStatusIdByKey('accepted')), receiver_id=user.id, is_active=1)

            if len(tasks) > 0:
                for task in tasks:
                    if task is not None:
                        dict_obj1 = {}
                        dict_obj1["user_id"] = user.id
                        dict_obj1["name"] = user.name
                        dict_obj1["task_type"] = task.task_type.name
                        dict_obj1["task_progress"] = task.progress
                        dict_obj1["task_name"] = task.name
                        dict_obj1["end_time"] = task.end_time
                        dict_obj1["leftdays"] = 12
                        # dict_obj1["leftdays"] = task.duration
                        dict_obj1["receive_status"] = task.receive_status
                        list_objects.append(dict_obj1)
            else:
                dict_obj2 = {}
                dict_obj2["user_id"] = user.id
                dict_obj2["name"] = user.name
                dict_obj2["task_type"] = ''
                dict_obj2["task_progress"] = ''
                dict_obj2["task_name"] = ''
                dict_obj2["end_time"] = ''
                dict_obj2["leftdays"] = ''
                dict_obj2["receive_status"] = ''
                list_objects.append(dict_obj2)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=list_objects)


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

            self.update_task(task_id, task_design_type_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id, task_design_type_id):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 任务负责人已接手,任务执行中
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('accepted')
                task.save()
                self.create_step(task_id, task_design_type_id)
                BusinessPublic.create_message(task.receiver.id, task.sender.id, menu_id=2,
                                              messages='任务负责人已接手,任务执行中!')

    def create_step(self, task_id, task_design_type_id):
        if task_id is not None:
            from business.models.step import Step
            from configuration.models import TaskStep, TaskDesignType

            task = Task.objects.get(id=task_id)
            task_design_type = TaskDesignType.objects.get(id=task_design_type_id)

            tasksteps = TaskStep.objects.filter(task_design_type_id=task_design_type_id)
            for taskstep in tasksteps:
                if taskstep:
                    step = Step(
                        name=taskstep.name,
                        index=taskstep.index,
                        task=task,
                        task_design_type=task_design_type,
                    )

                    step.save()


class TaskRejectView(APIView):
    """
    拒接任务
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
                # 任务负责人已拒接手
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('rejected')
                task.save()
                BusinessPublic.create_message(task.receiver.id, task.sender.id, menu_id=2,
                                              messages='任务负责人已拒接!')


class TaskAuditSubmitView(APIView):
    """
    任务提交验收
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
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_check')
                task.save()
                BusinessPublic.create_message(task.receiver.id, task.sender.id,menu_id=2,
                                              messages='有新的任务需要你的验收，请尽快处理!')


class TaskAuditSuccessView(APIView):
    """
    任务验收通过
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
                # 任务已完成
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('finished')
                task.save()
                BusinessPublic.create_message(task.receiver.id, task.sender.id,menu_id=2,
                                              messages='任务已通过验收!')


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
                receiver = UserProfile.objects.get(id=receiver_id)
                task.receiver = receiver
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_accept')
                task.save()

                BusinessPublic.create_reason(task.id, task.sender.id, task.receiver.id,
                                             BusinessPublic.GetReasonTypeIdByKey('task_allocate'),
                                             reason)
                BusinessPublic.create_message(task.receiver.id, task.sender.id,menu_id=2,
                                              messages='已安排新的任务,请查看!')
                self.update_step(task.id, task.sender.id)


    def update_step(self, task_id, receiver_id):
        if task_id is not None:
            from business.models.step import Step
            steps = Step.objects.filter(task_id=task_id)
            for step in steps:
                receiver = UserProfile.objects.get(id=receiver_id)
                step.receiver = receiver
                step.save()


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