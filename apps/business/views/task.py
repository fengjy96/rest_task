import datetime

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
from business.serializers.task_serializer import TaskSerializer, TaskListSerializer, TaskAllocateReasonSerializer
from utils.basic import MykeyResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import TaskFilter
from business.views.base import BusinessPublic
from business.models.project import Project
from business.models.step import Step
from business.models.files import Files, ProgressTexts
from configuration.models.task_conf import TaskStatus, TaskDesignType, TaskAssessment, TaskStep
from business.models.steplog import TaskLog
from points.models.projectpoints import ProjectPoints
from business.views.excel import Excel
from django.conf import settings
import uuid
import os


class TaskViewSet(ModelViewSet):
    """
    任务：增删改查
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('id',)
    filter_class = TaskFilter
    pagination_class = CommonPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """

        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer

    def create(self, request, *args, **kwargs):
        self.before_create(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        self.after_create(request, serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def before_create(self, request):
        # 任务创建人
        request.data['sender'] = request.user.id
        # 上级主管
        request.data['superior'] = request.user.id

        # 获取该任务所属的项目 id
        project_id = request.data.get('project', None)
        if project_id is None:
            raise Exception('项目 id 不能为空！')

        project = Project.objects.get(id=project_id)
        # 将项目负责人作为该任务的审核员
        if project.receiver_id is not None:
            request.data['auditor'] = project.receiver_id

        if request.data.get('receiver', None):
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('assigned')
        else:
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('unassigned')

    def after_create(self, request, serializer):
        project_id = request.data.get('project', None)
        project = Project.objects.get(id=project_id)

        # 富文本内容
        content = request.data.get('content', None)
        # 文件
        files = request.data.get('files', None)

        # - 更新相关项目信息
        self.update_project(project)

        # - 新增任务上传文件日志
        BusinessPublic.create_task_file_texts(serializer.data['id'], files, content)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = 0
        instance.save()

        # self.perform_destroy(instance)

        project_id = instance.project_id
        BusinessPublic.update_progress_by_project_id(project_id)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        self.before_update(request, kwargs)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        self.after_create(request, serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def before_update(self, request, kwargs):
        receiver_id = request.data.get('receiver', None)
        project_id = request.data.get('project', None)
        if project_id is None:
            raise Exception('项目 id 不能为空！')

        if receiver_id is not None:
            task_id = str(kwargs['pk'])
            task = Task.objects.get(id=task_id)
            # 如果当前任务已经存在负责人
            if task.receiver:
                if receiver_id != task.receiver.id:
                    if task.receive_status.id == TaskStatus.objects.get(key='accepted').id:
                        BusinessPublic.create_message(task.sender.id, task.receiver.id, menu_id=2,
                                                      messages='该任务已被项目负责人移走了!')
                    request.data['is_published'] = 0
                    request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('assigned')
            else:
                request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('assigned')
        else:
            request.data['receive_status'] = BusinessPublic.GetTaskStatusIdByKey('unassigned')

    def after_update(self, request, serializer):
        # 富文本内容
        content = request.data.get('content', None)
        # 文件
        files = request.data.get('files', None)
        # 新增任务上传文件日志
        BusinessPublic.create_task_file_texts(serializer.data['id'], files, content)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_active=1).order_by('-add_time').order_by('-task_priority_id')

        queryset = self.filter_list_queryset(request, queryset)

        queryset = self.filter_task(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def filter_task(self, request, queryset):
        """
        根据前端传递的查询参数过滤对应的任务
        :param request:
        :param queryset:
        :return:
        """
        q = Q()

        task_type_ids = request.query_params.get('task_type_ids', None)
        if task_type_ids:
            task_type_ids = task_type_ids.split(',')
            q.add(Q(task_type__in=task_type_ids), Q.AND)

        task_priority_ids = request.query_params.get('task_priority_ids', None)
        if task_priority_ids:
            task_priority_ids = task_priority_ids.split(',')
            q.add(Q(task_priority__in=task_priority_ids), Q.AND)

        task_quality_ids = request.query_params.get('task_quality_ids', None)
        if task_quality_ids:
            task_quality_ids = task_quality_ids.split(',')
            q.add(Q(task_quality__in=task_quality_ids), Q.AND)

        receive_status_ids = request.query_params.get('receive_status_ids', None)
        if receive_status_ids:
            receive_status_ids = receive_status_ids.split(',')
            q.add(Q(receive_status__in=receive_status_ids), Q.AND)

        audit_status_ids = request.query_params.get('audit_status_ids', None)
        if audit_status_ids:
            audit_status_ids = audit_status_ids.split(',')
            q.add(Q(audit_status__in=audit_status_ids), Q.AND)

        publish_status_ids = request.query_params.get('publish_status_ids', None)
        if publish_status_ids:
            publish_status_ids = publish_status_ids.split(',')
            q.add(Q(is_published__in=publish_status_ids), Q.AND)

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

        # 过滤任务接收者为 None 的数据，在任务发布大厅中显示
        has_receiver = request.query_params.get('has_receiver', None)
        if has_receiver == '0':
            queryset = queryset.filter(receiver__isnull=True)
            return queryset

        # 定义空的数据集
        emptyQuerySet = self.queryset.filter(is_active=999)
        queryset_task_auditor = emptyQuerySet
        queryset_project_manager = emptyQuerySet
        queryset_business_manager = emptyQuerySet
        queryset_project_auditor = emptyQuerySet

        # 获取当前用户 id
        user_id = request.user.id
        # 获取当前用户所属角色 id 列表
        user_role_list = self.get_user_roles(user_id)

        # 如果当前用户拥有管理员权限，则不做特殊处理
        if '系统管理员' in user_role_list:
            pass
        else:
            # 如果当前用户拥有任务负责人权限，则返回与该任务负责人关联的项目数据
            if '任务负责人' in user_role_list:
                queryset_project_manager = queryset.filter(Q(receiver_id=user_id) | Q(superior_id=user_id))
            # 如果当前用户拥有任务审核员（项目负责人）权限，则返回与该任务审核员（项目负责人）关联的项目数据
            if '项目负责人' in user_role_list:
                queryset_task_auditor = queryset.filter(auditor_id=user_id)
            # 如果当前用户拥有商务人员权限，则返回与该商务人员关联的项目数据
            if '商务人员' in user_role_list:
                queryset_business_manager = queryset
            if '项目审核员' in user_role_list:
                queryset_project_auditor = queryset

            queryset = queryset_task_auditor | queryset_project_manager | queryset_business_manager | queryset_project_auditor

        return queryset

    def get_user_roles(self, user_id):
        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)
            user_roles = user.roles.all()
            user_role_list = [role.name for role in user_roles]
            return user_role_list

    def update_project(self, project):
        # 更新项目状态
        self.update_project_status(project)
        # 更新项目进度
        self.update_project_progress(project.id)

    def update_project_status(self, project):
        # 如果项目状态为已完成，则当创建任务时，需要将项目状态调整为已接手
        if project.receive_status.key == 'finished':
            project.receive_status_id = BusinessPublic.GetProjectStatusIdByKey('accepted')
            project.save()

    def update_project_progress(self, project_id):
        # 更新项目进度
        BusinessPublic.update_progress_by_project_id(project_id)


class TaskNameView(APIView):
    """
    判断任务名是否存在
    """

    def post(self, request, format=None):
        name = request.data.get('name', None)
        project_id = request.data.get('project_id', None)
        task_id = request.data.get('task_id', None)

        if task_id is not None:
            cur_task = Task.objects.get(id=task_id)
            if name == cur_task.name:
                return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')

        if name is not None and project_id is not None:
            try:
                Task.objects.get(name=name, project_id=project_id)
                return MykeyResponse(status=status.HTTP_200_OK, data={'msg': '该任务名已存在，请重新输入'}, msg='请求成功')
            except Exception as e:
                return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')
        return MykeyResponse(status=status.HTTP_200_OK, data={}, msg='请求成功')


class TaskImportView(APIView):
    """
    上传单个Excel文件
    """

    def post(self, request):
        try:
            # 获取项目标识
            project_id = request.data.get('project_id', None)
            # 获取用户上传的文件,保存到服务器,再添加到数据库
            files = request.data.get('files', [])

            for file in files:
                path = '{}{}'.format(settings.BASE_DIR, file['url'])

                if os.path.exists(path):
                    datalist = Excel.import_excel_data(project_id, path)
                    os.remove(path)
                    return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=datalist)
                else:
                    return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='文件不存在')
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')


class TaskReceiverView(APIView):
    """
    获取任务负责人
    """

    def get(self, request, format=None):
        user_id = request.user.id

        user_role_list = self.get_user_roles(user_id)
        users = UserProfile.objects.filter(superior_id=user_id)

        users = self.filter_user(request, users)

        sign = True

        if '项目负责人' in user_role_list:
            sign = True
        elif '任务负责人' in user_role_list:
            sign = False

        list_objects = []

        if sign:
            for user in users:
                user_obj = {}
                user_obj["id"] = user.id
                user_obj["name"] = user.name
                list_objects.append(user_obj)
        else:
            for user in users:
                # tasks = Task.objects.filter(receiver_id=user.id, is_active=1, receive_status__lte=3)
                tasks = Task.objects.filter(~Q(receive_status=BusinessPublic.GetTaskStatusIdByKey('checked')),
                                            receiver_id=user.id, is_active=1)

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
                            dict_obj1["leftdays"] = (task.end_time - datetime.datetime.now().date()).days + 1
                            dict_obj1["receive_status"] = task.receive_status.text
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

    def get_user_roles(self, user_id):
        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)
            user_roles = user.roles.all()
            user_role_list = [role.name for role in user_roles]
            return user_role_list

    def filter_user(self, request, queryset):
        q = Q()

        task_type_ids = request.query_params.get('task_type_ids', None)
        if task_type_ids:
            task_type_ids = task_type_ids.split(',')
            q.add(Q(skills__in=task_type_ids), Q.AND)

        queryset = queryset.filter(q)

        return queryset.distinct()


class TaskAcceptView(APIView):
    """
    接手任务
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id', None)
            # 任务设计类型标识
            task_design_type_id = request.data.get('task_design_type_id', None)

            self.update_task(request, task_id, task_design_type_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, request, task_id, task_design_type_id):
        if task_id is not None and task_design_type_id is not None:
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 任务负责人已接手，任务执行中
                task.receive_status = TaskStatus.objects.get(key='accepted')
                if task.receiver is None:
                    task.receiver = request.user
                task.task_design_type = TaskDesignType.objects.get(id=task_design_type_id)
                task.save()
                self.create_step(task_id, task_design_type_id, request.user)
                BusinessPublic.create_message(task.receiver.id, task.sender.id, menu_id=2,
                                              messages='任务负责人已接手,任务执行中!')

    def create_step(self, task_id, task_design_type_id, receiver):
        if task_id is not None and task_design_type_id is not None and receiver:
            task = Task.objects.get(id=task_id)
            task_design_type = TaskDesignType.objects.get(id=task_design_type_id)

            tasksteps = TaskStep.objects.filter(task_design_type_id=task_design_type_id)
            for taskstep in tasksteps:
                if taskstep:
                    # step = Step.objects.filter(task_id=task.id, name=taskstep.name, task_design_type_id=taskstep.task_design_type.id)
                    # if not step.exists():
                    Step.objects.create(name=taskstep.name, index=taskstep.index, task=task,
                                        task_design_type=task_design_type, receiver=receiver)


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


class TaskCheckSubmitView(APIView):
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
                BusinessPublic.create_message(task.receiver.id, task.sender.id, menu_id=2,
                                              messages='有新的任务需要你的验收，请尽快处理!')


class TaskCheckPassView(APIView):
    """
    任务验收通过
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id', None)
            # 评级
            task_assessment_id = request.data.get('task_assessment_id', None)
            # 评语
            comments = request.data.get('comments', None)

            self.update_task(task_id, task_assessment_id, comments)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id, assessment_id, comments):
        if task_id is not None:
            if assessment_id is not None and comments is not None:
                assessment = TaskAssessment.objects.get(id=assessment_id)
                task = Task.objects.get(id=task_id)
                if task is not None:
                    # 任务已通过验收
                    task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('checked')
                    task.task_assessment = assessment
                    task.comments = comments
                    task.save()

                    project_id = task.project_id
                    BusinessPublic.update_progress_by_project_id(project_id)

                BusinessPublic.create_message(task.sender.id, task.receiver.id, menu_id=2,
                                              messages='任务已通过验收!')


class TaskCheckRejectView(APIView):
    """
    项目验收不通过
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_id = request.data.get('task_id')
            # 验收不通过原因
            reason = request.data.get('reason') or ''

            self.update_task(task_id, reason)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id, reason):
        if task_id is not None:
            from business.models.task import Task
            task = Task.objects.get(id=task_id)
            if task is not None:
                # 任务验收不通过
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('check_rejected')
                task.save()
                BusinessPublic.create_reason(task.id, task.receiver.id, task.sender.id,
                                             BusinessPublic.GetReasonTypeIdByKey('task_check_reject'),
                                             reason)
                BusinessPublic.create_message(task.receiver.id, task.sender.id, menu_id=2,
                                              messages='任务验收不通过')


class TaskAllocateView(APIView):
    """
    任务转派
    """

    def post(self, request, format=None):
        try:
            # 任务标识
            task_ids = request.data.get('task_ids', [])
            # 接收者标识
            receiver_id = request.data.get('receiver_id')

            self.update_task(request, task_ids, receiver_id)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, request, task_ids, receiver_id):
        if len(task_ids) > 0:
            for task_id in task_ids:
                from business.models.task import Task
                task = Task.objects.get(id=task_id)
                if task is not None:
                    old_receiver_id = task.receiver.id
                    receiver = UserProfile.objects.get(id=receiver_id)
                    task.receiver = receiver
                    task.superior_id = request.user.id
                    task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_accept')
                    task.save()
                    if old_receiver_id != receiver_id:
                        # 转移积分
                        ProjectPoints.objects.filter(user_id=task.receiver.id, is_created=0,
                                                     project_id=task.project.id).update(user_id=receiver_id)
                    BusinessPublic.create_message(task.superior.id, task.receiver.id, menu_id=2,
                                                  messages='已安排新的任务,请查看!')


class TaskFileIsEmptyViewSet(ModelViewSet):
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
    filterset_fields = ('task_id', 'receiver_id')
    ordering_fields = ('id',)
    # permission_classes = [IsAuthenticated]


class TaskLogsView(APIView):
    """
    查询单条任务的日志
    """

    def get(self, request, format=None):
        try:
            # 任务标识
            task_id = request.query_params.get('task_id')

            # 获取任务日志
            task_logs = self.get_task_logs(task_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=task_logs)

    def get_task_logs(self, id):
        """
        获取任务日志
        """
        task_logs_list = []

        task_logs = TaskLog.objects.filter(task_id=id).order_by("-add_time")
        for task_log in task_logs:
            log_obj = {}
            log_obj['id'] = task_log.id
            log_obj['add_time'] = task_log.add_time
            log_obj['files'] = self.get_task_log_files(task_log.id)
            task_logs_list.append(log_obj)

        return task_logs_list

    def get_task_log_files(self, id):
        """
        日志文件列表
        """
        task_log_file_list = []

        files = Files.objects.filter(tasklog_id=id)
        for file in files:
            log_file_obj = {}
            log_file_obj['id'] = file.id
            log_file_obj['name'] = file.name
            log_file_obj['path'] = file.path
            log_file_obj['path_thumb_w200'] = file.path_thumb_w200
            log_file_obj['path_thumb_w900'] = file.path_thumb_w900
            log_file_obj['type'] = 1
            log_file_obj['add_time'] = file.add_time
            task_log_file_list.append(log_file_obj)

        progresstexts = ProgressTexts.objects.filter(tasklog_id=id)
        for progresstext in progresstexts:
            log_text_obj = {}
            log_text_obj['id'] = progresstext.id
            log_text_obj['content'] = progresstext.content
            log_text_obj["type"] = 0
            log_text_obj['add_time'] = progresstext.add_time
            task_log_file_list.append(log_text_obj)

        return task_log_file_list


class TaskPublishView(APIView):
    """任务发布"""

    def post(self, request, format=None):
        try:
            # 任务 id 列表
            task_ids = request.data.get('selected_task_ids', [])
            if task_ids and len(task_ids) > 0:
                for task_id in task_ids:
                    self.update_task(task_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_task(self, task_id):
        if task_id is not None:
            task = Task.objects.filter(id=task_id, is_published=0).first()
            if task:
                task.is_published = 1
                task.publish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                task.receive_status = BusinessPublic.GetTaskStatusObjectByKey('wait_accept')
                task.save()

                if task.receiver:
                    # 新增消息
                    BusinessPublic.create_message(task.sender.id, task.receiver.id, menu_id=2,
                                                  messages='已安排新的任务,请查看!')
