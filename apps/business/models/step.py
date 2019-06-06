from datetime import datetime

from django.db import models

from business.models.task import Task
from configuration.models import TaskDesignType
from rbac.models import Company, UserProfile


class Step(models.Model):
    """
    任务步骤
    """
    company = models.ForeignKey(Company, null=True, blank=True,verbose_name='公司标识', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, blank=True, verbose_name='任务标识', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=80, verbose_name='步骤名称')
    index = models.IntegerField(null=True, blank=True,verbose_name='步骤序号')
    progress = models.IntegerField(verbose_name='步骤进度', default=0)
    task_design_type = models.ForeignKey(TaskDesignType, null=True, blank=True, verbose_name='设计方式', on_delete=models.CASCADE)

    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    is_finished = models.IntegerField(default=0, verbose_name='是否完成')

    sender = models.ForeignKey(UserProfile, null=True, blank=True,verbose_name='发送者', on_delete=models.CASCADE, related_name='step_sender')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True,verbose_name='接收者', on_delete=models.CASCADE, related_name='step_receiver')
    # receive_status = models.IntegerField(default=0, verbose_name='接收状态')
    auditor = models.ForeignKey(UserProfile, null=True, blank=True,verbose_name='审核员', on_delete=models.CASCADE, related_name='step_auditor')
    audit_status = models.IntegerField(default=0, verbose_name='审核状态')

    begin_time = models.DateField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateField(null=True, blank=True, verbose_name='结束时间')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name


class StepRejectReason(models.Model):
    """
    任务步骤驳回原因表模型：当发生步骤驳回时，用于存储任务驳回原因
    """
    step = models.ForeignKey(Step, null=True, blank=True, verbose_name='步骤标识', on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, default='', verbose_name='驳回原因')
    transfer_nums = models.IntegerField(default=0, verbose_name='驳回次数')

    sender = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='发送者', on_delete=models.CASCADE,
                               related_name='step_reject_reason_sender')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='接收者', on_delete=models.CASCADE,
                                 related_name='step_reject_reason_receiver')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = '步骤驳回原因'
        verbose_name_plural = verbose_name
