from django.db import models
from rbac.models import UserProfile
from business.models.project import Project
from business.models.task import Task
from rbac.models import Role

class ProjectPoints(models.Model):
    """
    项目积分表模型
    """
    user = models.ForeignKey(to=UserProfile, null=True, blank=True, verbose_name='用户标识', on_delete=models.CASCADE, related_name='project_points_user_id')
    project = models.ForeignKey(to=Project, null=True, blank=True, verbose_name='项目标识', on_delete=models.CASCADE, related_name='project_points_project_id')
    task = models.ForeignKey(to=Task, null=True, blank=True, verbose_name='任务标识', on_delete=models.CASCADE, related_name='project_points_task_id')
    role = models.ForeignKey(to=Role, null=True, blank=True, verbose_name='任务标识', on_delete=models.CASCADE,related_name='project_points_task_id')
    points = models.IntegerField(default=0, verbose_name='积分')
    type_id = models.IntegerField(default=0, verbose_name='积分类型')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')

    def __str__(self):
        return self.points

    class Meta:
        verbose_name = '项目积分'
        verbose_name_plural = verbose_name
