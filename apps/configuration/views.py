from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from configuration.models import (
    TaskStep, TaskAssessment, TaskPriority, TaskQuality,
    TaskDesignType, TaskType, Skill, Salary)
from .serializers import (
    TaskTypeSerializer, TaskStepSerializer, TaskAssessmentSerializer,
    TaskPrioritySerializer, TaskQualitySerializer, TaskDesignTypeSerializer, SkillSerializer, SalarySerializer)


class TaskTypeViewSet(ModelViewSet):
    """
    任务类型：增删改查
    """
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
    permission_classes = (IsAuthenticated,)


class TaskStepViewSet(ModelViewSet):
    """
    任务步骤：增删改查
    """
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer
    permission_classes = (IsAuthenticated,)


class TaskAssessmentViewSet(ModelViewSet):
    """
    任务评估
    """
    queryset = TaskAssessment.objects.all()
    serializer_class = TaskAssessmentSerializer
    permission_classes = (IsAuthenticated,)


class TaskPriorityViewSet(ModelViewSet):
    """
    任务优先级：增删改查
    """
    queryset = TaskPriority.objects.all()
    serializer_class = TaskPrioritySerializer
    permission_classes = (IsAuthenticated,)


class TaskQualityViewSet(ModelViewSet):
    """
    任务质量：增删改查
    """
    queryset = TaskQuality.objects.all()
    serializer_class = TaskQualitySerializer
    permission_classes = (IsAuthenticated,)


class TaskDesignTypeViewSet(ModelViewSet):
    """
    任务设计类型：增删改查
    """
    queryset = TaskDesignType.objects.all()
    serializer_class = TaskDesignTypeSerializer
    permission_classes = (IsAuthenticated,)


class SalaryViewSet(ModelViewSet):
    """
    用户薪水：增删改查
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = (IsAuthenticated,)


class SkillViewSet(ModelViewSet):
    """
    用户技能：增删改查
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticated,)
