from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import CommonPagination
from configuration.filters import TaskStepFilter
from configuration.models.project_conf import ProjectStatus
from configuration.models.task_conf import TaskStep, TaskAssessment, TaskPriority, TaskQuality, TaskDesignType, TaskType, TaskStatus
from configuration.models.reason_conf import ReasonType
from .serializers import (
    TaskTypeSerializer, TaskStepSerializer, TaskAssessmentSerializer,
    TaskPrioritySerializer, TaskQualitySerializer, TaskDesignTypeSerializer,
    ProjectStatusSerializer, TaskStatusSerializer, ReasonTypeSerializer, TaskDesignTypeListSerializer,
    TaskStepListSerializer)


class ReasonTypeViewSet(ModelViewSet):
    """
    原因类型：增删改查
    """

    pagination_class = CommonPagination
    # 获取查询集
    queryset = ReasonType.objects.all()
    serializer_class = ReasonTypeSerializer
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class ProjectStatusViewSet(ModelViewSet):
    """
    项目状态：增删改查
    """

    pagination_class = CommonPagination
    # 获取查询集
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer
    # 指定过滤 backends
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('index',)
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class TaskStatusViewSet(ModelViewSet):
    """
    任务状态：增删改查
    """

    pagination_class = CommonPagination
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    # 指定过滤 backends
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = ('index',)
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)


class TaskTypeViewSet(ModelViewSet):
    """
    任务类型：增删改查
    """

    pagination_class = CommonPagination
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
    permission_classes = (IsAuthenticated,)


class TaskStepViewSet(ModelViewSet):
    """
    任务步骤：增删改查
    """

    queryset = TaskStep.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)
    filterset_class = TaskStepFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = CommonPagination
    serializer_class = TaskStepSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskStepListSerializer
        return TaskStepSerializer


class TaskAssessmentViewSet(ModelViewSet):
    """
    任务评估
    """

    pagination_class = CommonPagination
    queryset = TaskAssessment.objects.all()
    serializer_class = TaskAssessmentSerializer
    permission_classes = (IsAuthenticated,)


class TaskPriorityViewSet(ModelViewSet):
    """
    任务优先级：增删改查
    """

    pagination_class = CommonPagination
    queryset = TaskPriority.objects.all()
    serializer_class = TaskPrioritySerializer
    permission_classes = (IsAuthenticated,)


class TaskQualityViewSet(ModelViewSet):
    """
    任务质量：增删改查
    """

    pagination_class = CommonPagination
    queryset = TaskQuality.objects.all()
    serializer_class = TaskQualitySerializer
    permission_classes = (IsAuthenticated,)


class TaskDesignTypeViewSet(ModelViewSet):
    """
    任务设计类型：增删改查
    """

    pagination_class = CommonPagination
    queryset = TaskDesignType.objects.all()
    serializer_class = TaskDesignTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('task_type',)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskDesignTypeListSerializer
        return TaskDesignTypeSerializer
