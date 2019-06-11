from django.db import models

from rbac.models import UserProfile


class PointsDetail(models.Model):
    """
    积分表模型
    """
    user = models.ForeignKey(to=UserProfile, null=True, blank=True, verbose_name='用户标识', on_delete=models.CASCADE)
    operation_points = models.IntegerField(default=0, verbose_name='本次操作的积分')
    available_points = models.IntegerField(default=0, verbose_name='可用积分')
    operation_type = models.IntegerField(null=True, blank=True,  verbose_name='操作类型')
    points_type = models.IntegerField(null=True, blank=True,  verbose_name='积分类型')
    points_status = models.IntegerField(default=1, verbose_name='积分状态')
    points_source = models.IntegerField(null=True, blank=True,  verbose_name='积分来源')
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='添加时间')

    def __str__(self):
        return self.operation_points

    class Meta:
        verbose_name = '用户积分明细'
        verbose_name_plural = verbose_name
