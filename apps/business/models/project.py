from datetime import datetime

from django.db import models

from rbac.models import Company, UserProfile
from configuration.models import TaskType

class Project(models.Model):
    """
    项目表模型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=80, verbose_name='项目名')
    style = models.CharField(default='', max_length=80, verbose_name='项目风格')
    progress = models.IntegerField(default=0, verbose_name='项目进度')
    points = models.IntegerField(default=0, verbose_name='项目积分')
    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    is_finished = models.IntegerField(default=0, verbose_name='是否完成')
    customer = models.CharField(default='', max_length=80, verbose_name='客户')

    sender = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='发送者', on_delete=models.CASCADE, related_name='project_sender')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='接收者', on_delete=models.CASCADE, related_name='project_receiver')
    receive_status = models.IntegerField(default=0, verbose_name='接收状态')
    auditor = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='审核员', on_delete=models.CASCADE, related_name='project_auditor')
    audit_status = models.IntegerField(default=0, verbose_name='审核状态')

    begin_time = models.DateField(null=True, blank=True, verbose_name='项目开始时间')
    end_time = models.DateField(null=True, blank=True, verbose_name='项目结束时间')
    duration = models.FloatField(default=0, verbose_name='项目时长')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    delete_time = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name


class ProjectRejectReason(models.Model):
    """
    项目驳回原因表模型
    """
    project = models.ForeignKey(Project, verbose_name='项目标识', on_delete=models.CASCADE,related_name='project_reject_reason_project_id')
    reason = models.CharField(default='', max_length=80, verbose_name='项目驳回原因')
    transfer_nums = models.IntegerField(default=0, verbose_name='驳回次数')

    sender = models.ForeignKey(UserProfile, verbose_name='发送者', on_delete=models.CASCADE,
                               related_name='project_reject_reason_sender_id')
    receiver = models.ForeignKey(UserProfile, verbose_name='接收者', on_delete=models.CASCADE,
                                 related_name='project_reject_reason_receiver_id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = '项目驳回原因'
        verbose_name_plural = verbose_name


class ProjectFee(models.Model):
    """
    用于计算员工成本
    """
    company = models.ForeignKey(Company, verbose_name='公司标识', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name='项目标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='费用名称')
    value = models.FloatField(verbose_name='费用')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '费用项'
        verbose_name_plural = verbose_name

class ProjectCost(models.Model):
    """
    项目成本
    """
    project_id = models.IntegerField(verbose_name='项目标识')
    task_id = models.IntegerField(verbose_name='任务标识')
    task_type = models.ForeignKey(TaskType, verbose_name='任务类型', on_delete=models.CASCADE, related_name='project_cost_task_type_id')
    user = models.ForeignKey(UserProfile, verbose_name='用户标识', on_delete=models.CASCADE, related_name='project_cost_user_id')
    person_nums = models.IntegerField(verbose_name='人数')
    duration = models.IntegerField(verbose_name=' 时限')
    name = models.CharField(max_length=80, verbose_name='费用名称')
    fee = models.FloatField(verbose_name='费用')
    total_fee = models.FloatField(verbose_name='总费用')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目成本'
        verbose_name_plural = verbose_name