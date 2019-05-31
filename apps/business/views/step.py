from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from business.models.step import Step
from business.serializers.step_serializer import StepSerializer, StepListSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import StepFilter
from rest_framework.views import APIView
from business.models.files import Files, FeedBacks, ProgressTexts, FeedBackTexts
from business.models.steplog import StepLog, FeedBackLog
from common.custom import CommonPagination
from utils.basic import MykeyResponse

from .base import BusinessPublic


class StepViewSet(ModelViewSet):
    """
    任务步骤：增删改查
    """

    queryset = Step.objects.all()
    serializer_class = StepSerializer
    ordering_fields = ('id',)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 指定筛选类
    filter_class = StepFilter
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
        if self.action == 'list':
            return StepListSerializer
        return StepSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
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


class StepProgressUpdateView(APIView):
    """
    步骤进度更新
    """

    def post(self, request):
        try:
            # 步骤标识
            step_id = request.data.get('step_id', None)
            # 标题
            title = request.data.get('title', None)
            # 进度
            progress = request.data.get('progress', None)
            # 备注
            memo = request.data.get('memo', None)
            # 富文本内容
            content = request.data.get('content', None)
            # 文件
            files = request.data.get('files', None)

            # 增加步骤日志
            if step_id is not None and title is not None and progress is not None:
                step_log = StepLog(step_id=step_id, title=title, progress=progress, memo=memo)
                step_log.save()

                if files:
                    for file in files:
                        # 增加文件表记录
                        step_log_file = Files(steplog=step_log, name=file['name'], path=file['url'])
                        step_log_file.save()

                # 如果存在富文本，则先添加富文本
                if content:
                    progresstexts = ProgressTexts(steplog=step_log, content=content)
                    progresstexts.save()

                # 更新步骤进度
                step = Step.objects.get(id=step_id)
                if step:
                    step.progress = progress
                    step.save()
                    self.updateProgress(step_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def updateProgress(self, step_id):
        """
        更新进度
        :return:
        """
        BusinessPublic.update_task_progress(step_id)
        BusinessPublic.update_project_progress(step_id)


class StepProgressUpdateLogsView(APIView):
    """
    查询单条步骤的进度更新日志
    """

    def get(self, request, format=None):
        try:
            # 步骤标识
            step_id = request.query_params.get('step_id')

            # 获取步骤日志
            step_logs = self.get_step_logs(step_id)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_logs)

    def get_step_logs(self, id):
        """
        获取步骤日志
        """
        step_logs_list = []

        step_logs = StepLog.objects.filter(step_id=id).order_by("-add_time")
        for step_log in step_logs:
            log_obj = {}
            log_obj['id'] = step_log.id
            log_obj['title'] = step_log.title
            log_obj['progress'] = step_log.progress
            log_obj['add_time'] = step_log.add_time
            log_obj['files'] = self.get_step_log_files(step_log.id)
            step_logs_list.append(log_obj)

        return step_logs_list

    def get_step_log_files(self, id):
        """
        日志文件列表
        """
        step_log_file_list = []

        files = Files.objects.filter(steplog_id=id)
        for file in files:
            log_file_obj = {}
            log_file_obj['id'] = file.id
            log_file_obj['name'] = file.name
            log_file_obj['path'] = file.path
            log_file_obj['type'] = 1
            log_file_obj['add_time'] = file.add_time
            log_file_obj["feedbacks"] = self.get_feedback_logs(file.id, 1)
            step_log_file_list.append(log_file_obj)

        progresstexts = ProgressTexts.objects.filter(steplog_id=id)
        for progresstext in progresstexts:
            log_text_obj = {}
            log_text_obj['id'] = progresstext.id
            log_text_obj['content'] = progresstext.content
            log_text_obj["type"] = 0
            log_text_obj['add_time'] = progresstext.add_time
            log_text_obj["feedbacks"] = self.get_feedback_logs(progresstext.id, 0)
            step_log_file_list.append(log_text_obj)

        return step_log_file_list

    def get_feedback_logs(self, id, type):
        """
        反馈日志
        """
        feedback_logs_list = []

        feedback_logs = FeedBackLog.objects.filter(step_log_file_id=id, type=type).order_by('-add_time')
        for feedback_log in feedback_logs:
            log_file_obj = {}
            log_file_obj['id'] = feedback_log.id
            log_file_obj['title'] = feedback_log.title
            log_file_obj['memo'] = feedback_log.memo
            log_file_obj['add_time'] = feedback_log.add_time
            log_file_obj["files"] = self.get_feedback_log_files(feedback_log.id)
            feedback_logs_list.append(log_file_obj)

        return feedback_logs_list

    def get_feedback_log_files(self, id):
        """
        反馈文件
        """
        feedback_log_file_list = []

        feedback_log_files = FeedBacks.objects.filter(feedbacklog_id=id)
        for log_file in feedback_log_files:
            log_file_obj = {}
            log_file_obj['id'] = log_file.id
            log_file_obj['name'] = log_file.name
            log_file_obj['path'] = log_file.path
            log_file_obj['type'] = 1
            log_file_obj['add_time'] = log_file.add_time
            feedback_log_file_list.append(log_file_obj)


        feedback_log_contents = FeedBackTexts.objects.filter(feedbacklog_id=id)
        for log_content in feedback_log_contents:
            log_text_obj = {}
            log_text_obj['id'] = log_content.id
            log_text_obj['content'] = log_content.content
            log_text_obj['type'] = 0
            log_text_obj['add_time'] = log_content.add_time
            feedback_log_file_list.append(log_text_obj)

        return feedback_log_file_list


class StepLogFileFeedBackUpdateView(APIView):
    """
    增加反馈日志，反馈文件，反馈富文本
    """

    def post(self, request):
        try:
            # 文件或者富文本标识
            step_log_file_id = request.data.get('step_log_file_id', None)
            # 类型
            type = request.data.get('type', None)
            # 标题
            title = request.data.get('title', None)
            # 备注
            memo = request.data.get('memo', None)
            # 内容
            content = request.data.get('content', None)
            # 文件列表
            files = request.data.get('files', None)

            # 增加日志
            if step_log_file_id is not None and type is not None and title is not None:
                feedback_log = FeedBackLog(step_log_file_id=step_log_file_id, type=type, title=title, memo=memo)
                feedback_log.save()

                if files:
                    for file in files:
                        # 增加文件表记录
                        feedback_file = FeedBacks(feedbacklog=feedback_log, name=file['name'], path=file['url'])
                        feedback_file.save()

                # 如果存在反馈富文本,则先添加反馈富文本
                if content:
                    feedback_log_contents = FeedBackTexts(feedbacklog=feedback_log, content=content)
                    feedback_log_contents.save()

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')


class StepLogFileFeedBackLogView(APIView):
    """
    单个文件以及富文本预览以及查看反馈
    """

    def get(self, request, format=None):
        try:
            # 文件标识
            file_id = request.query_params.get('file_id', None)
            # 类型
            type = request.query_params.get('type', None)

            if file_id is not None and type is not None:
                if type == '1':
                    step_log_file_list = self.one_get_step_log_files(file_id)
                else:
                    step_log_file_list = self.one_progresstext_objects(file_id)
                return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_log_file_list)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)

    def one_get_step_log_files(self, id):
        """
        单个文件以及反馈日志
        """
        feedback_logs = []

        file = Files.objects.get(id=id)
        if file:
            feedback_logs = self.get_feedback_logs(file.id, 1)

        return feedback_logs

    def one_progresstext_objects(self, id):
        """
        单个文件以及反馈日志
        """
        feedback_logs = []

        progresstext = ProgressTexts.objects.get(id=id)
        if progresstext:
            feedback_logs = self.get_feedback_logs(progresstext.id, 0)

        return feedback_logs

    def get_feedback_logs(self, id, type):
        """
        获取反馈日志
        """
        feedback_logs_list = []

        feedback_logs = FeedBackLog.objects.filter(step_log_file_id=id, type=type).order_by('-add_time')
        for feedback_log in feedback_logs:
            log_obj = {}
            log_obj['id'] = feedback_log.id
            log_obj['title'] = feedback_log.title
            log_obj['memo'] = feedback_log.memo
            log_obj['add_time'] = feedback_log.add_time
            log_obj["files"] = self.get_feedback_log_files(feedback_log.id)
            feedback_logs_list.append(log_obj)

        return feedback_logs_list

    def get_feedback_log_files(self, id):
        """
        获取反馈日志文件
        """
        feedback_log_file_list = []

        feedback_log_files = FeedBacks.objects.filter(feedbacklog_id=id)
        for file in feedback_log_files:
            file_obj = {}
            file_obj['id'] = file.id
            file_obj['name'] = file.name
            file_obj['path'] = file.path
            file_obj['type'] = 1
            file_obj['add_time'] = file.add_time
            feedback_log_file_list.append(file_obj)

        feedback_log_contents = FeedBackTexts.objects.filter(feedbacklog_id=id)
        for log_content in feedback_log_contents:
            text_obj = {}
            text_obj['id'] = log_content.id
            text_obj['content'] = log_content.content
            text_obj['add_time'] = log_content.add_time
            text_obj['type'] = 0
            feedback_log_file_list.append(text_obj)

        return feedback_log_file_list
