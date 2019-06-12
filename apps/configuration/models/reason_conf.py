from django.db import models


class ReasonType(models.Model):
    """
    原因类型
    """
    key = models.CharField(max_length=30, verbose_name='类型英文表示')
    text = models.CharField(max_length=30, verbose_name='类型中文表示')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '原因类型'
        verbose_name_plural = verbose_name
