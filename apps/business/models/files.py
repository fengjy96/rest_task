from django.db import models
from business.models.steplog import StepLog, FeedBackLog, TaskLog


class Files(models.Model):
    """
    文件模型
    """

    tasklog = models.ForeignKey(TaskLog, null=True, blank=True, verbose_name='任务日志标识', on_delete=models.CASCADE)
    steplog = models.ForeignKey(StepLog, null=True, blank=True, verbose_name='步骤日志标识', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=150, verbose_name='文件名称')
    path = models.CharField(default='', max_length=300, verbose_name='文件路径')
    path_thumb_w200 = models.CharField(default='', max_length=300, verbose_name='宽度为 200 的缩略图文件路径（只针对图片）')
    path_thumb_w900 = models.CharField(default='', max_length=300, verbose_name='宽度为 900 的缩略图文件路径（只针对图片）')
    type = models.IntegerField(default=1, verbose_name='类型')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = verbose_name


class ProgressTexts(models.Model):
    """
    进度富文本模型
    """
    tasklog = models.ForeignKey(TaskLog, null=True, blank=True, verbose_name='任务日志标识', on_delete=models.CASCADE)
    steplog = models.ForeignKey(StepLog, null=True, blank=True, verbose_name='日志标识', on_delete=models.CASCADE)
    type = models.IntegerField(default=0, verbose_name='类型')
    content = models.TextField(default='', verbose_name='内容')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '富文本'
        verbose_name_plural = verbose_name


class FeedBacks(models.Model):
    """
    反馈文件模型
    """
    feedbacklog = models.ForeignKey(FeedBackLog, null=True, blank=True, verbose_name='日志文件标识', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=150, verbose_name='文件名称')
    path = models.CharField(default='', max_length=300, verbose_name='文件路径')
    path_thumb_w200 = models.CharField(default='', max_length=300, verbose_name='宽度为 200 的缩略图文件路径（只针对图片）')
    path_thumb_w900 = models.CharField(default='', max_length=300, verbose_name='宽度为 900 的缩略图文件路径（只针对图片）')
    type = models.IntegerField(default=1, verbose_name='类型')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = verbose_name


class FeedBackTexts(models.Model):
    """
    反馈富文本模型
    """
    feedbacklog = models.ForeignKey(FeedBackLog, null=True, blank=True, verbose_name='日志文件标识', on_delete=models.CASCADE)
    type = models.IntegerField(default=0, verbose_name='类型')
    content = models.TextField(default='', verbose_name='内容')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '反馈富文本'
