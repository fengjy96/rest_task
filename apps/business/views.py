from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from business.models.project import Project, ProjectFee, ProjectRejectReason
from business.models.task import Task, TaskAllocateReason
from business.models.step import Step, StepRejectReason
from business.models.message import Message

from business.serializers import (
    ProjectSerializer, ProjectFeeSerializer, ProjectRejectReasonSerializer, TaskAllocateReasonSerializer,
    TaskSerializer, MessageSerializer, StepRejectReasonSerializer, StepSerializer)


class ProjectViewSet(ModelViewSet):
    """
    项目：增删改查
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)


class ProjectFeeViewSet(ModelViewSet):
    """
    项目费用：增删改查
    """
    queryset = ProjectFee.objects.all()
    serializer_class = ProjectFeeSerializer
    permission_classes = (IsAuthenticated,)


class ProjectRejectReasonViewSet(ModelViewSet):
    """
    项目拒绝原因：增删改查
    """
    queryset = ProjectRejectReason.objects.all()
    serializer_class = ProjectRejectReasonSerializer
    permission_classes = (IsAuthenticated,)


class TaskViewSet(ModelViewSet):
    """
    任务：增删改查
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskAllocateReasonViewSet(ModelViewSet):
    """
    任务分派原因：增删改查
    """
    queryset = TaskAllocateReason.objects.all()
    serializer_class = TaskAllocateReasonSerializer
    permission_classes = (IsAuthenticated,)


class StepViewSet(ModelViewSet):
    """
    任务步骤：增删改查
    """
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (IsAuthenticated,)


class StepRejectReasonViewSet(ModelViewSet):
    """
    任务步骤拒绝原因：增删改查
    """
    queryset = StepRejectReason.objects.all()
    serializer_class = StepRejectReasonSerializer
    permission_classes = (IsAuthenticated,)


class MessageViewSet(ModelViewSet):
    """
    消息：增删改查
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
