from django.db import models
from business.models.task import Task
from datetime import datetime
from business.models.steplog import StepLog, FeedBackLog

class Files(models.Model):
    """
    文件模型
    """
    task = models.ForeignKey(Task, null=True, blank=True,verbose_name='任务标识', on_delete=models.CASCADE)
    steplog = models.ForeignKey(StepLog, null=True, blank=True,verbose_name='日志标识', on_delete=models.CASCADE)
    name = models.CharField(default='',max_length=150, verbose_name='文件名称')
    path = models.CharField(default='',max_length=300, verbose_name='文件路径')
    type = models.IntegerField(default=1, verbose_name='类型')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = verbose_name

class ProgressTexts(models.Model):
    """
    进度富文本模型
    """
    steplog = models.ForeignKey(StepLog, null=True, blank=True,verbose_name='日志标识', on_delete=models.CASCADE)
    type = models.IntegerField(default=0, verbose_name='类型')
    content = models.TextField(default='',max_length=80, verbose_name='内容')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '富文本'
        verbose_name_plural = verbose_name

class FeedBacks(models.Model):
    """
    反馈文件模型
    """
    feedbacklog = models.ForeignKey(FeedBackLog, null=True, blank=True,verbose_name='日志文件标识', on_delete=models.CASCADE)
    name = models.CharField(default='',max_length=150, verbose_name='文件名称')
    path = models.CharField(default='',max_length=300, verbose_name='文件路径')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = verbose_name

class FeedBackTexts(models.Model):
    """
    反馈富文本模型
    """
    feedbacklog = models.ForeignKey(FeedBackLog, null=True, blank=True,verbose_name='日志文件标识', on_delete=models.CASCADE)
    type = models.IntegerField(default=0, verbose_name='类型')
    content = models.TextField(default='',max_length=80, verbose_name='内容')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '反馈富文本'

