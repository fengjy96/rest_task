from django.db import models


class ProjectStatus(models.Model):
    """
    项目状态
    """
    index = models.IntegerField(verbose_name='排序')
    value = models.IntegerField(verbose_name='状态真实序号')
    key = models.CharField(max_length=30, verbose_name='状态英文表示')
    text = models.CharField(max_length=30, verbose_name='状态中文表示')
    desc = models.CharField(max_length=50, default='', verbose_name='状态描述')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '项目状态'
        verbose_name_plural = verbose_name


class Fee(models.Model):
    """
    基本费用表
    """
    name = models.CharField(max_length=80, verbose_name='费用名称')
    value = models.IntegerField(verbose_name='费用', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '基本费用'
        verbose_name_plural = verbose_name
