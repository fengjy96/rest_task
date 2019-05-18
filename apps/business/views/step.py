from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from business.models.step import Step
from business.serializers.step_serializer import StepSerializer, StepListSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.views.filters import StepFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from business.models.files import Files, FeedBacks, ProgressTexts, FeedBackTexts
from business.models.steplog import StepLog, FeedBackLog
from utils.basic import MykeyResponse

step_objects_data = []
steplog_objects_data = []
file_objects_data = []
# progresstext_objects_data = []
feedbacklog_objects_data = []
feedback_objects_data = []
# feedbacktext_objects_data = []

class StepViewSet(ModelViewSet):
    """
    任务步骤：增删改查
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    # permission_classes = (IsAuthenticated,)


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

class StepLogFilePreviewView(APIView):
    """
    预览以及查看反馈
    """
    def get(self, request, format=None):
        # 文件标识
        file_id = request.data.get('file_id')
        # 类型
        type= request.data.get('type')

        if type == 0:
            file_objects(file_id)
        else:
            progresstext_objects(file_id)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_objects_data)

class StepsLogsView(APIView):
    """
    一条步骤
    """
    def get(self, request, format=None):
        # 步骤标识
        step_id = request.data.get('step_id')

        steplog_objects(step_id)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_objects_data)


class StepsViewSet(APIView):
    """
    步骤以及日志
    """
    def get(self, request, format=None):
        # 任务标识
        task_id = request.data.get('task_id')

        step_objects(task_id)

        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=step_objects_data)

def step_objects(self, task_id=0):
    """
    步骤
    """
    steps = Step.objects.filter(task_id=task_id)
    for step in steps:
        dict_obj1 = {}
        dict_obj1["id"] = step.id

        dict_obj2 = {}
        dict_obj2["id"] = step.company.id
        dict_obj2["name"] = step.company.name

        dict_obj3 = {}
        dict_obj3["id"] = step.task.id
        dict_obj3["name"] = step.task.name

        dict_obj4 = {}
        dict_obj4["id"] = step.task_design_type.id
        dict_obj4["name"] = step.task_design_type.name

        dict_obj5 = {}
        dict_obj5["id"] = step.sender.id
        dict_obj5["name"] = step.sender.name

        dict_obj6 = {}
        dict_obj6["id"] = step.receiver.id
        dict_obj6["name"] = step.receiver.name

        dict_obj7 = {}
        dict_obj7["id"] = step.auditor.id
        dict_obj7["name"] = step.auditor.name

        dict_obj1["company"] = dict_obj2
        dict_obj1["task_id"] = dict_obj3
        dict_obj1["name"] = step.name
        dict_obj1["index"] = step.index
        dict_obj1["progress"] = step.progress
        dict_obj1["task_design_type"] = dict_obj4
        dict_obj1["is_active"] = step.is_active
        dict_obj1["is_finished"] = step.is_finished
        dict_obj1["sender"] = dict_obj5
        dict_obj1["send_status"] = step.send_status
        dict_obj1["receiver"] = dict_obj6
        dict_obj1["receive_status"] = step.receive_status
        dict_obj1["auditor"] = dict_obj7
        dict_obj1["audit_status"] = step.audit_status

        self.steplog_objects(step.id)
        dict_obj1["logs"] = steplogs_objects

        step_objects_data.append(dict_obj1)

def steplogs_objects(self, id=0):
    """
    时间轴日志列表
    """
    steplogs = StepLog.objects.filter(step_id=id)
    if steplogs is not None:
        for steplog in steplogs:
            if steplog is not None:
                dict_obj = {}
                dict_obj["id"] = steplog.id
                dict_obj["title"] = steplog.title
                dict_obj["progress"] = steplog.progress
                dict_obj["memo"] = steplog.memo
                dict_obj["add_time"] = steplog.add_time

                self.files_objects(steplog.id)
                self.progresstext_objects(steplog.id)
                dict_obj["files"] = file_objects_data

                steplog_objects_data.append(dict_obj)

def steplog_objects(self, id=0):
    """
    单条时间轴日志
    """
    steplog = StepLog.objects.get(id=id)
    if steplog is not None:
        dict_obj = {}
        dict_obj["id"] = steplog.id
        dict_obj["title"] = steplog.title
        dict_obj["progress"] = steplog.progress
        dict_obj["memo"] = steplog.memo
        dict_obj["add_time"] = steplog.add_time

        self.file_objects(steplog.id)
        self.progresstext_objects(steplog.id)
        dict_obj["files"] = file_objects_data

        steplog_objects_data.append(dict_obj)

def files_objects(self, id=0):
    """
    日志文件列表
    """
    files = Files.objects.filter(steplog_id=id)
    if files is not None:
        for file in files:
            if file is not None:
                dict_obj = {}
                dict_obj["id"] = file.id
                dict_obj["name"] = file.name
                dict_obj["path"] = file.path
                dict_obj["type"] = 1
                dict_obj["content"] = ""
                dict_obj["add_time"] = file.add_time

                self.feedbacklog_objects(file.id)
                dict_obj["feedbacks"] = feedbacklog_objects_data

                file_objects_data.append(dict_obj)

def file_objects(self, id=0):
    """
    单条日志文件
    """
    file = Files.objects.get(id=id)
    if file is not None:
        dict_obj = {}
        dict_obj["id"] = file.id
        dict_obj["name"] = file.name
        dict_obj["path"] = file.path
        dict_obj["type"] = 1
        dict_obj["content"] = ""
        dict_obj["add_time"] = file.add_time

        self.feedbacklog_objects(file.id)
        dict_obj["feedbacks"] = feedbacklog_objects_data

        file_objects_data.append(dict_obj)

def progresstext_objects(self, id=0):
    """
    进度富文本
    """
    progresstext = ProgressTexts.objects.get(steplog_id=id)
    if progresstext is not None:
        dict_obj = {}
        dict_obj["id"] = progresstext.id
        dict_obj["name"] = ""
        dict_obj["path"] = ""
        dict_obj["type"] = 1
        dict_obj["content"] = progresstext.content
        dict_obj["add_time"] = progresstext.add_time

        self.feedbacklog_objects(progresstext.id)
        dict_obj["feedbacks"] = feedbacklog_objects_data

        file_objects_data.append(dict_obj)

def feedbacklog_objects(self, id=0):
    """
    反馈日志
    """
    FeedBackLogs = FeedBackLog.objects.filter(feebacklog_id=id)
    if FeedBackLogs is not None:
        for feedbacklog in FeedBackLogs:
            if feedbacklog is not None:
                dict_obj = {}
                dict_obj["id"] = feedbacklog.id
                dict_obj["title"] = feedbacklog.title
                dict_obj["memo"] = feedbacklog.memo
                dict_obj["add_time"] = feedbacklog.add_time

                self.feedback_objects(feedbacklog.id)
                self.feedbacktext_objects(feedbacklog.id)
                dict_obj["files"] = feedback_objects_data

                feedbacklog_objects_data.append(dict_obj)

def feedback_objects(self, id=0):
    """
    反馈文件
    """
    feedbacks = FeedBacks.objects.filter(feebacklog_id=id)
    if feedbacks is not None:
        for feedback in feedbacks:
            if feedback is not None:
                dict_obj = {}
                dict_obj["id"] = feedback.id
                dict_obj["name"] = feedback.name
                dict_obj["path"] = feedback.path
                dict_obj["type"] = 1
                dict_obj["content"] = ""
                dict_obj["add_time"] = feedback.add_time

                feedback_objects_data.append(dict_obj)

def feedbacktext_objects(self, id=0):
    """
    反馈富文本
    """
    feeBacktexts = FeedBackTexts.objects.get(file_id=id)
    if feeBacktexts is not None:
        dict_obj = {}
        dict_obj["id"] = feeBacktexts.id
        dict_obj["name"] = ""
        dict_obj["path"] = ""
        dict_obj["type"] = 1
        dict_obj["content"] = feeBacktexts.content
        dict_obj["add_time"] = feeBacktexts.add_time

        feedback_objects_data.append(dict_obj)
