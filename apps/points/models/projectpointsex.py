from django.db import models
from business.models.project import Project

class ProjectPointsEx(models.Model):
    """
    项目积分附加表模型
    """

    project = models.ForeignKey(to=Project, null=True, blank=True, verbose_name='项目标识', on_delete=models.CASCADE, related_name='project_points_ex_project_id')
    points = models.IntegerField(default=0, verbose_name='积分')
    left_points = models.IntegerField(default=0, verbose_name='剩余积分')
    project_receiver_percentage = models.IntegerField(default=0, verbose_name='项目负责人百分比')
    project_sender_percentage = models.IntegerField(default=0, verbose_name='商务人员百分比')

    def __str__(self):
        return self.points

    class Meta:
        verbose_name = '项目积分附加表'
        verbose_name_plural = verbose_name
