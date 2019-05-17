from django.db import models

from rbac.models import UserProfile


class ProjectPoints(models.Model):
    """
    积分表模型
    """
    user = models.ForeignKey(to=UserProfile, verbose_name='用户标识', on_delete=models.CASCADE)
    points = models.IntegerField(verbose_name='积分')
    link_id = models.IntegerField(verbose_name='项目或者任务标识')
    type_id = models.IntegerField(verbose_name='积分类型')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')

    def __str__(self):
        return self.points

    class Meta:
        verbose_name = '项目积分'
        verbose_name_plural = verbose_name
