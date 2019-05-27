from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from business.models.step import Step
from business.serializers.step_serializer import StepSerializer, StepListSerializer, StepCreateSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import StepFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from business.models.files import Files, FeedBacks, ProgressTexts, FeedBackTexts
from business.models.steplog import StepLog, FeedBackLog
from common.custom import CommonPagination
from utils.basic import MykeyResponse

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
        if self.action == 'create':
            return StepCreateSerializer
        elif self.action == 'list':
            return StepListSerializer
        return StepSerializer

    def create(self, request, *args, **kwargs):
        # request.data['sender'] = request.user.id
        # if request.data['receiver']:
        #     request.data['receive_status'] = 1
        # else:
        #     request.data['receive_status'] = 0
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # if request.data['receiver']:
        #     request.data['receive_status'] = 1
        # else:
        #     request.data['receive_status'] = 0
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


class StepListView(ListAPIView):
    """
    任务步骤：增删改查
    """
    queryset = Step.objects.all()
    serializer_class = StepListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = StepFilter
    ordering_fields = ('id',)

    def get_queryset(self):
        # 步骤状态值为激活
        is_active = 1

        return Step.objects.filter(is_active=is_active)

class StepLogFileFeedBacksView(APIView):
    """
    单个文件以及富文本预览以及查看反馈
    """
    def get(self, request, format=None):
        try:
            # 文件标识
            file_id = request.data.get('file_id')
            # 类型
            type= request.data.get('type')

            if type == 0:
                file_objects_data = one_file_objects(file_id)
            else:
                file_objects_data = one_progresstext_objects(file_id)

        except Exception as e:
                return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=file_objects_data)

class StepsLogsView(APIView):
    """
    查询单条步骤以及日志
    """
    def get(self, request, format=None):
        try:
            # 步骤标识
            step_id = request.data.get('step_id')

            step_objects_data = steplog_objects(step_id)

        except Exception as e:
                return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_objects_data)

class StepsViewSet(APIView):
    """
    查询所有步骤以及日志
    """
    def get(self, request, format=None):
        # 任务标识
        try:
            task_id = request.data.get('task_id')

            step_objects_data = step_objects(task_id)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_objects_data)

def step_objects(task_id):
    """
    步骤
    """
    step_objects_data = []

    steps = Step.objects.filter(task_id=task_id,is_active=1)
    for step in steps:
        if step:
            dict_obj = {}
            dict_obj["id"] = step.id

            dict_obj_company = {}
            if step.company:
                dict_obj_company["id"] = step.company.id
                dict_obj_company["name"] = step.company.name

            dict_obj_task = {}
            if step.task:
                dict_obj_task["id"] = step.task.id
                dict_obj_task["name"] = step.task.name

            dict_obj_design_type = {}
            if step.task_design_type:
                dict_obj_design_type["id"] = step.task_design_type.id
                dict_obj_design_type["name"] = step.task_design_type.name

            dict_obj_sender = {}
            if step.sender:
                dict_obj_sender["id"] = step.sender.id
                dict_obj_sender["name"] = step.sender.name

            dict_obj_receiver = {}
            if step.receiver:
                dict_obj_receiver["id"] = step.receiver.id
                dict_obj_receiver["name"] = step.receiver.name

            dict_obj_auditor = {}
            if step.auditor:
                dict_obj_auditor["id"] = step.auditor.id
                dict_obj_auditor["name"] = step.auditor.name

            dict_obj["company"] = dict_obj_company
            dict_obj["task_id"] = dict_obj_task
            dict_obj["name"] = step.name

            if step.index:
                dict_obj["index"] = step.index
            else:
                dict_obj["index"] = ''

            dict_obj["progress"] = step.progress
            dict_obj["task_design_type"] = dict_obj_design_type
            dict_obj["is_active"] = step.is_active
            dict_obj["is_finished"] = step.is_finished
            dict_obj["sender"] = dict_obj_sender
            dict_obj["send_status"] = step.send_status
            dict_obj["receiver"] = dict_obj_receiver
            dict_obj["receive_status"] = step.receive_status
            dict_obj["auditor"] = dict_obj_auditor
            dict_obj["audit_status"] = step.audit_status

            dict_obj["logs"] = steplogs_objects(step.id)

            step_objects_data.append(dict_obj)

    return step_objects_data

def steplogs_objects(id):
    """
    时间轴日志列表
    """
    steplog_objects_data = []

    steplogs = StepLog.objects.filter(step_id=id)
    if steplogs:
        for steplog in steplogs:
            if steplog:
                dict_obj = {}
                dict_obj["id"] = steplog.id
                dict_obj["title"] = steplog.title
                dict_obj["progress"] = steplog.progress
                dict_obj["memo"] = steplog.memo
                dict_obj["add_time"] = steplog.add_time

                dict_obj["files"] = files_objects(steplog.id)

                steplog_objects_data.append(dict_obj)

    return steplog_objects_data

def files_objects(id):
    """
    日志文件列表
    """
    file_objects_data = []

    files = Files.objects.filter(steplog_id=id)
    if files:
        for file in files:
            if file:
                dict_obj = {}
                dict_obj["id"] = file.id
                dict_obj["name"] = file.name
                dict_obj["path"] = file.path
                dict_obj["type"] = 1
                dict_obj["content"] = ''
                dict_obj["add_time"] = file.add_time

                dict_obj["feedbacks"] = feedbacklog_objects(file.id,1)

                file_objects_data.append(dict_obj)

    progresstexts = ProgressTexts.objects.filter(steplog_id=id)
    if progresstexts:
        for progresstext in progresstexts:
             if progresstext:
                 dict_obj = {}
                 dict_obj["id"] = progresstext.id
                 dict_obj["name"] = ''
                 dict_obj["path"] = ''
                 dict_obj["type"] = 0
                 dict_obj["content"] = progresstext.content
                 dict_obj["add_time"] = progresstext.add_time

                 dict_obj["feedbacks"] = feedbacklog_objects(progresstext.id,0)

                 file_objects_data.append(dict_obj)

    return file_objects_data

def feedbacklog_objects(id,type):
    """
    反馈日志
    """
    feedbacklog_objects_data = []

    FeedBackLogs = FeedBackLog.objects.filter(link_id=id,type=type)
    if FeedBackLogs:
        for feedbacklog in FeedBackLogs:
            if feedbacklog:
                dict_obj = {}
                dict_obj["id"] = feedbacklog.id
                dict_obj["title"] = feedbacklog.title
                dict_obj["memo"] = feedbacklog.memo
                dict_obj["add_time"] = feedbacklog.add_time

                dict_obj["files"] = feedback_objects(feedbacklog.id)

                feedbacklog_objects_data.append(dict_obj)

    return feedbacklog_objects_data

def feedback_objects(id):
    """
    反馈文件
    """
    feedback_objects_data = []

    feedbacks = FeedBacks.objects.filter(feedbacklog_id=id)
    if feedbacks:
        for feedback in feedbacks:
            if feedback:
                dict_obj = {}
                dict_obj["id"] = feedback.id
                dict_obj["name"] = feedback.name
                dict_obj["path"] = feedback.path
                dict_obj["type"] = 1
                dict_obj["content"] = ''
                dict_obj["add_time"] = feedback.add_time

                feedback_objects_data.append(dict_obj)

    feedbacktexts = FeedBackTexts.objects.filter(feedbacklog_id=id)
    if feedbacktexts:
         for feedbacktext in feedbacktexts:
              if feedbacktext:
                    dict_obj = {}
                    dict_obj["id"] = feedbacktext.id
                    dict_obj["name"] = ''
                    dict_obj["path"] = ''
                    dict_obj["type"] = 0
                    dict_obj["content"] = feedbacktext.content
                    dict_obj["add_time"] = feedbacktext.add_time

                    feedback_objects_data.append(dict_obj)

    return feedback_objects_data


def steplog_objects(id):
    """
    单条时间轴日志
    """
    steplog_objects_data = []

    steplogs = StepLog.objects.filter(id=id)
    if steplogs:
        for steplog in steplogs:
            if steplog:
                dict_obj = {}
                dict_obj["id"] = steplog.id
                dict_obj["title"] = steplog.title
                dict_obj["progress"] = steplog.progress
                dict_obj["memo"] = steplog.memo
                dict_obj["add_time"] = steplog.add_time

                dict_obj["files"] = files_objects(steplog.id)

                steplog_objects_data.append(dict_obj)

    return steplog_objects_data

def one_file_objects(id):
    """
    单个文件以及反馈日志
    """
    file_objects_data = []

    files = Files.objects.filter(id=id)
    if files:
        for file in files:
             if file:
                 dict_obj = {}
                 dict_obj["id"] = file.id
                 dict_obj["name"] = file.name
                 dict_obj["path"] = file.path
                 dict_obj["type"] = 1
                 dict_obj["content"] = ''
                 dict_obj["add_time"] = file.add_time


                 dict_obj["feedbacks"] = feedbacklog_objects(file.id,1)

                 file_objects_data.append(dict_obj)

    return file_objects_data

def one_progresstext_objects(id):
    """
    单个文件以及反馈日志
    """
    file_objects_data = []

    progresstexts = ProgressTexts.objects.filter(id=id)
    if progresstexts:
        for progresstext in progresstexts:
             if progresstext:
                 dict_obj = {}
                 dict_obj["id"] = progresstext.id
                 dict_obj["name"] = ''
                 dict_obj["path"] = ''
                 dict_obj["type"] = 0
                 dict_obj["content"] = progresstext.content
                 dict_obj["add_time"] = progresstext.add_time

                 dict_obj["feedbacks"] = feedbacklog_objects(progresstext.id,0)

                 file_objects_data.append(dict_obj)

    return file_objects_data