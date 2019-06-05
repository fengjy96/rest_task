from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from configuration.models import (
    TaskStep, TaskAssessment, TaskPriority, TaskQuality,
    TaskDesignType, TaskType, Skill, Salary, ProjectStatus, TaskStatus, ReasonType)
from .serializers import (
    TaskTypeSerializer, TaskStepSerializer, TaskAssessmentSerializer,
    TaskPrioritySerializer, TaskQualitySerializer, TaskDesignTypeSerializer, SkillSerializer, SalarySerializer,
    ProjectStatusSerializer, TaskStatusSerializer, ReasonTypeSerializer)


class ReasonTypeViewSet(ModelViewSet):
    """
    原因类型：增删改查
    """

    # 获取查询集
    queryset = ReasonType.objects.all()
    serializer_class = ReasonTypeSerializer
    # 指定授权类
    # permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectStatusViewSet(ModelViewSet):
    """
    项目状态：增删改查
    """

    # 获取查询集
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer
    # 指定过滤 backends
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('index',)
    # 指定授权类
    # permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class TaskStatusViewSet(ModelViewSet):
    """
    任务状态：增删改查
    """

    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    # 指定过滤 backends
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = ('index',)
    # 指定授权类
    # permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('task_type_id',)
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
