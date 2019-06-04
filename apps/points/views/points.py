from rest_framework import status
from points.models.projectpoints import ProjectPoints
from business.models.project import Project
from business.models.task import Task
from configuration.models import TaskPriority
from configuration.models import TaskQuality
from utils.basic import MykeyResponse
from rbac.models import UserProfile, Role
from rest_framework.generics import ListAPIView
from points.serializers import ProjectPointsSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from common.custom import CommonPagination


class PointsAssignmentView(ListAPIView):
    """
    项目积分分配
    """

    queryset = ProjectPoints.objects.all()
    serializer_class = ProjectPointsSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('project_id',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id', None)
            # 项目负责人百分比
            project_receiver_percentage = request.data.get('project_receiver_percentage', None)
            # 商务人员百分比
            project_sender_percentage = request.data.get('project_sender_percentage', None)
            # 项目总积分
            project_points = request.data.get('project_points', None)

            self.create_project_receiver_points(project_id, project_points, project_receiver_percentage)
            self.create_project_sender_points(project_id, project_points, project_sender_percentage)
            self.create_task_receiver_points(project_id, project_points, project_receiver_percentage,
                                             project_sender_percentage)

            queryset = self.filter_queryset(self.get_queryset()).filter(project_id=project_id)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功', data=serializer.data)

    def create_project_receiver_points(self, project_id, project_points, project_receiver_percentage):
        """
        创建项目负责人积分
        """
        if project_id is not None and project_points is not None and project_receiver_percentage is not None:
            project = Project.objects.get(id=project_id, is_active=1)
            if project is not None:
                points = (int(project_points) * int(project_receiver_percentage)) / 100
                points = int(points)

                self.create_project_points(project.id, project.receiver.id, points, 0, 7)

    def create_project_sender_points(self, project_id, project_points, project_sender_percentage):
        """
        创建商务人员积分
        """
        if project_id is not None and project_points is not None and project_sender_percentage is not None:
            project = Project.objects.get(id=project_id, is_active=1)
            if project is not None:
                points = (int(project_points) * int(project_sender_percentage)) / 100
                points = int(points)

                self.create_project_points(project.id, project.sender.id, points, 0, 8)

    def create_task_receiver_points(self, project_id, project_points, project_receiver_percentage,
                                    project_sender_percentage):
        if project_id is not None and project_points is not None and project_receiver_percentage is not None and project_sender_percentage is not None:
            # 项目负责人积分
            project_receiver_points = (int(project_points) * int(project_receiver_percentage)) / 100
            project_receiver_points = int(project_receiver_points)
            # 商务人员积分
            project_sender_points = (int(project_points) * int(project_receiver_percentage)) / 100
            project_sender_points = int(project_sender_points)

            # 剩余积分=总积分-项目负责人积分-商务人员积分
            project_left_points = int(project_points) - project_receiver_points - project_sender_points

            # 任务总权重
            totalweight = 0.0

            tasks = Task.objects.filter(project=project_id, is_active=1)
            for task in tasks:
                if task is not None:
                    # 取任务的优先级以及品质要求的权重
                    if task.task_priority:
                        taskpriority = TaskPriority.objects.get(id=task.task_priority.id)
                        if task.task_quality:
                            taskquality = TaskQuality.objects.get(id=task.task_quality.id)
                            taskweight = taskpriority.weight * taskquality.weight
                            taskweight = round(taskweight, 2)
                            totalweight = totalweight + taskweight

            for task in tasks:
                if task is not None:
                    # 取任务的优先级以及品质要求的权重
                    if task.task_priority:
                        taskpriority = TaskPriority.objects.get(id=task.task_priority.id)
                        if task.task_quality:
                            taskquality = TaskQuality.objects.get(id=task.task_quality.id)
                            taskweight = taskpriority.weight * taskquality.weight
                            task_weight_percentage = round(taskweight / totalweight, 2)
                            points = int(task_weight_percentage * project_left_points)

                            self.create_task_points(project_id, task.id, task.receiver.id, points, 1, 6)

    def create_project_points(self, project_id, user_id, points, type_id, role_id):
        """
        如果项目积分表中存在记录则更新，如果没有则新增
        :param project_id:项目标识
        :param user_id:用户标识
        :param points:积分
        :param type_id:0:项目 1:任务
        :return:
        """
        # task = None
        user = UserProfile.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        role = Role.objects.get(id=role_id)

        projectpoints = ProjectPoints.objects.filter(project_id=project_id, type_id=type_id, user_id=user_id,
                                                     role_id=role_id)
        if projectpoints.exists():
            projectpoint = ProjectPoints.objects.get(project_id=project_id, type_id=type_id, user_id=user_id,
                                                     role_id=role_id)
            projectpoint.project = project
            projectpoint.user = user
            projectpoint.role = role
            projectpoint.points = points
            projectpoint.type_id = type_id

            projectpoint.save()
        else:
            ProjectPoints.objects.create(project=project, type_id=type_id, user=user, points=points, role=role)

    def create_task_points(self, project_id, task_id, user_id, points, type_id, role_id):
        """
        如果项目积分表中存在记录则更新，如果没有则新增
        :param project_id:项目标识
        :param task_id:任务标识
        :param user_id:用户标识
        :param points:积分
        :param type_id:0:项目 1:任务
        :return:
        """
        # task = None
        user = UserProfile.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        role = Role.objects.get(id=role_id)

        if task_id != 0:
            task = Task.objects.get(id=task_id)

            projectpoints = ProjectPoints.objects.filter(project_id=project_id, task_id=task_id, type_id=type_id,
                                                         user_id=user_id, role_id=role_id)
            if projectpoints.exists():
                projectpoint = ProjectPoints.objects.get(project_id=project_id, task_id=task_id, type_id=type_id,
                                                         user_id=user_id, role_id=role_id)
                projectpoint.project = project
                projectpoint.task = task
                projectpoint.user = user
                projectpoint.role = role
                projectpoint.points = points
                projectpoint.type_id = type_id
                projectpoint.save()
            else:
                ProjectPoints.objects.create(project=project, task=task, type_id=type_id, user=user, points=points,
                                             role=role)
