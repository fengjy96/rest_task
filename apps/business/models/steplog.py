from django.db import models
from business.models.step import Step
from datetime import datetime

class StepLog(models.Model):
    """
    步骤日志模型
    """
    step = models.ForeignKey(Step, verbose_name='步骤标识', on_delete=models.CASCADE)
    title = models.CharField(default='',max_length=150, verbose_name='标题')
    progress = models.IntegerField(default=0, verbose_name='进度')
    memo = models.CharField(default='',max_length=300, verbose_name='备注')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '步骤日志'
        verbose_name_plural = verbose_name

class FeedBackLog(models.Model):
    """
    反馈日志模型
    """
    linkid = models.IntegerField(default=0, verbose_name='关链标识')
    title = models.CharField(default='',max_length=150, verbose_name='标题')
    memo = models.CharField(default='',max_length=300, verbose_name='备注')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '反馈日志'
        verbose_name_plural = verbose_name
