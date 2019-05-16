from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from points.models.points import Points
from points.models.projectpoints import ProjectPoints
from points.models.pointsdetail import PointsDetail
from business.models.project import Project
from business.models.task import Task
from configuration.models import TaskPriority
from configuration.models import TaskQuality

from points.serializers import (
    PointsSerializer, PointsDetailSerializer, ProjectPointsSerializer)
from utils.basic import MykeyResponse


class PointsViewSet(ModelViewSet):
    """
    积分：增删改查
    """
    queryset = Points.objects.all()
    serializer_class = PointsSerializer
    permission_classes = (IsAuthenticated,)

class ProjectPointsViewSet(ModelViewSet):
    """
    积分：增删改查
    """
    queryset = ProjectPoints.objects.all()
    serializer_class = ProjectPointsSerializer
    permission_classes = (IsAuthenticated,)


class PointsDetailViewSet(ModelViewSet):
    """
    积分明细：增删改查
    """
    queryset = PointsDetail.objects.all()
    serializer_class = PointsDetailSerializer
    permission_classes = (IsAuthenticated,)


class PointsAssignmentView(APIView):
    """
    项目积分分配
    """

    def post(self, request, format=None):
        try:
            # 项目标识
            project_id = request.data.get('project_id')

            # 项目百分比
            project_percentage = request.data.get('project_percentage')

            # 项目总积分
            project_points = request.data.get('project_points')

            self.create_project_receiver_points(project_id, project_points, project_percentage)
            self.create_task_receiver_points(project_id, project_points, project_percentage)

        except Exception as e:
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg='请求失败')
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def create_project_receiver_points(self, project_id, project_points, project_percentage):
        """
        创建项目负责人积分
        :param project_id:
        :param project_points:
        :param project_percentage:
        :return:
        """
        project = Project.objects.filter(id=project_id, is_active=1)
        points = (project_points * project_percentage) / 100
        points = int(points)

        self.create_project_task_points(project.id, project.receiver, points)

    def create_task_receiver_points(self, project_id, project_points, project_percentage):
        if project_id is not None:
            # 计算项目经理的积分
            project_receiver_points = (project_points * project_percentage) / 100
            project_receiver_points = int(project_receiver_points)

            # 计算剩余积分
            project_left_points = project_points - project_receiver_points

            # 总权重
            totalweight = 0.0

            tasks = Task.objects.filter(project=project_id, is_active=1)
            for task in tasks:
                if task is not None:
                    # 取任务的优先级以及品质要求的权重
                    taskpriority = TaskPriority.objects.get(task.task_priority)
                    taskquality = TaskQuality.objects.get(task.task_quality)

                    taskweight = taskpriority * taskquality

                    taskweight = round(taskweight, 2)

                    totalweight = totalweight + taskweight

            averageweight = project_left_points / totalweight

            # 平均权重
            averageweight = round(averageweight, 2)

            for task in tasks:
                if task is not None:
                    # 取任务的优先级以及品质要求的权重
                    taskpriority = TaskPriority.objects.get(task.task_priority)
                    taskquality = TaskQuality.objects.get(task.task_quality)

                    taskweight = taskpriority * taskquality

                    taskweight = round(taskweight, 2)

                    points = int(taskweight * averageweight)

                    self.create_project_task_points(task.id, task.receiver, points)

    def create_project_task_points(self, task_id, user_id, points):
        """
        在项目积分表中新增一条记录
        :param task_id:
        :param user_id:
        :param points:
        :return:
        """
        projectpoint = ProjectPoints(
            user_id=user_id,
            points=points,
            link_id=task_id,
            type_id=1,
            is_active=1
        )
        projectpoint.save()
