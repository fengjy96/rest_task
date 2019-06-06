from django.db import models

from configuration.models import TaskType, TaskPriority, TaskQuality, TaskAssessment, TaskDesignType, TaskStatus
from business.models.project import Project
from rbac.models import Company, UserProfile


class Task(models.Model):
    """
    任务表模型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=80, verbose_name='任务名称')
    task_type = models.ForeignKey(TaskType, null=True, blank=True, verbose_name='任务类型标识', on_delete=models.CASCADE)
    task_design_type = models.ForeignKey(TaskDesignType, null=True, blank=True, verbose_name='设计方式',
                                         on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True, verbose_name='任务内容')
    progress = models.IntegerField(default=0, verbose_name='任务进度')
    task_priority = models.ForeignKey(TaskPriority, null=True, blank=True, verbose_name='任务优先级', on_delete=models.CASCADE)
    task_quality = models.ForeignKey(TaskQuality, null=True, blank=True, verbose_name='任务质量', on_delete=models.CASCADE)

    begin_time = models.DateField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateField(null=True, blank=True, verbose_name='结束时间')

    task_assessment = models.ForeignKey(TaskAssessment, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name='任务评级')
    comments = models.CharField(default='', max_length=80, null=True, blank=True, verbose_name='任务评语')
    points = models.IntegerField(default=0, verbose_name='任务积分')

    memo = models.CharField(null=True, blank=True, max_length=800, verbose_name='任务备注')

    project = models.ForeignKey(Project, null=True, blank=True, verbose_name='项目标识', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='发送者', on_delete=models.CASCADE,
                               related_name='task_sender')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='接收者', on_delete=models.CASCADE,
                                 related_name='task_receiver')
    receive_status = models.ForeignKey(TaskStatus, null=True, blank=True, verbose_name='任务状态', on_delete=models.CASCADE,
                                       related_name='task_receive_status')
    auditor = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='审核员', on_delete=models.CASCADE,
                                related_name='task_auditor')
    audit_status = models.IntegerField(null=True, blank=True, verbose_name='审核状态')

    is_active = models.IntegerField(default=1, verbose_name='是否激活')
    is_finished = models.IntegerField(default=0, verbose_name='是否完成')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    finish_time = models.DateTimeField(auto_now=True, verbose_name='完成时间')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目任务'
        verbose_name_plural = verbose_name


class TaskAllocateReason(models.Model):
    """
    任务备注表模型：当发生任务转派时，用于存储转派原因
    """
    task = models.ForeignKey(Task, null=True, blank=True, verbose_name='任务标识', on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, default='', verbose_name='转派原因')
    transfer_nums = models.IntegerField(default=0, verbose_name='流转次数')

    sender = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='发送者', on_delete=models.CASCADE,
                               related_name='task_allocate_reason_sender')
    receiver = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='接收者', on_delete=models.CASCADE,
                                 related_name='task_allocate_reason_receiver')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = '任务转派原因'
        verbose_name_plural = verbose_name
