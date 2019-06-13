from django.db import models
from rbac.models import UserProfile
from configuration.models.reason_conf import ReasonType

class Reason(models.Model):
    """
    原因表模型
    """
    type = models.ForeignKey(ReasonType, null=True, blank=True, verbose_name='原因类型', on_delete=models.CASCADE,
                               related_name='reason_type')
    link_id = models.IntegerField(default=1, verbose_name='关链标识')
    reason = models.CharField(default='', max_length=180, verbose_name='原因')
    transfer_nums = models.IntegerField(default=0, verbose_name='次数')
    sender = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='发送者', on_delete=models.CASCADE,
                               related_name='reason_sender_id')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='接收者', on_delete=models.CASCADE,
                                 related_name='reason_receiver_id')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = '原因'
        verbose_name_plural = verbose_name