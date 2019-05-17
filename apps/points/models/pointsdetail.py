from django.db import models

from rbac.models import UserProfile


class PointsDetail(models.Model):
    """
    积分表模型
    """
    user = models.ForeignKey(to=UserProfile, verbose_name='用户标识', on_delete=models.CASCADE)
    operation_points = models.IntegerField(verbose_name='本次操作的积分')
    available_points = models.IntegerField(verbose_name='可用积分')
    operation_type = models.IntegerField(verbose_name='操作类型')
    points_type = models.IntegerField(verbose_name='积分类型')
    points_status = models.IntegerField(verbose_name='积分状态')
    points_source = models.IntegerField(verbose_name='积分来源')

    def __str__(self):
        return self.operation_points

    class Meta:
        verbose_name = '用户积分明细'
        verbose_name_plural = verbose_name
