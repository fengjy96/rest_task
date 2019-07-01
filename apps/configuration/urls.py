from django.urls import path, include

from rest_framework import routers

from configuration.views import (
    TaskTypeViewSet, TaskDesignTypeViewSet, TaskPriorityViewSet, TaskQualityViewSet,
    TaskStepViewSet, ProjectStatusViewSet, TaskStatusViewSet, ReasonTypeViewSet, TaskAssessmentViewSet)

# 创建路由器并注册相关视图
router = routers.DefaultRouter()
router.register('reason_types', ReasonTypeViewSet, basename='reason_types')
router.register('project_statuses', ProjectStatusViewSet, basename='project_statuses')
router.register('task_statuses', TaskStatusViewSet, basename='task_statuses')
router.register('task_types', TaskTypeViewSet, basename='task_types')
router.register('task_design_types', TaskDesignTypeViewSet, basename='task_design_types')
router.register('task_priorities', TaskPriorityViewSet, basename='task_priorities')
router.register('task_qualities', TaskQualityViewSet, basename='task_qualities')
router.register('task_steps', TaskStepViewSet, basename='task_steps')
router.register('task_assessments', TaskAssessmentViewSet, basename='task_assessments')

urlpatterns = [
    # API
    path(r'api/v1/', include(router.urls))
]
