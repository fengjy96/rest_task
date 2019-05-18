from django.db import models
from datetime import datetime
from rbac.models import UserProfile
from rbac.models import Menu

class Message(models.Model):
    """
    消息表模型
    """
    type = models.CharField(max_length=80, verbose_name='类型')
    title = models.CharField(max_length=80, verbose_name='标题')
    content = models.CharField(max_length=80, verbose_name='内容')
    sender = models.ForeignKey(to=UserProfile, verbose_name='发送者', on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(to=UserProfile, verbose_name='接收者', on_delete=models.CASCADE, related_name='message_receiver')
    status = models.IntegerField(verbose_name='状态')
    menu = models.ForeignKey(Menu, null=True, blank=True, verbose_name='菜单标识', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
