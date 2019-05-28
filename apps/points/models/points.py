from django.db import models

from rbac.models import UserProfile


class Points(models.Model):
    """
    积分表模型
    """
    user = models.ForeignKey(to=UserProfile, verbose_name='用户标识', on_delete=models.CASCADE)
    total_points = models.IntegerField(verbose_name='总积分')
    available_points = models.IntegerField(verbose_name='可用积分')

    def __str__(self):
        return self.total_points

    class Meta:
        verbose_name = '用户积分'
        verbose_name_plural = verbose_name
