from django.db import models

from rbac.models import Company, UserProfile


class ProjectStatus(models.Model):
    """
    项目状态
    """
    index = models.IntegerField(verbose_name='排序')
    value = models.IntegerField(verbose_name='状态真实序号')
    key = models.CharField(max_length=30, verbose_name='状态英文表示')
    text = models.CharField(max_length=30, verbose_name='状态中文表示')
    desc = models.CharField(max_length=50, null=True, blank=True, verbose_name='状态描述')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '项目状态'
        verbose_name_plural = verbose_name


class TaskStatus(models.Model):
    """
    任务状态
    """
    index = models.IntegerField(verbose_name='排序')
    value = models.IntegerField(verbose_name='状态真实序号')
    key = models.CharField(max_length=30, verbose_name='状态英文表示')
    text = models.CharField(max_length=30, verbose_name='状态中文表示')
    desc = models.CharField(max_length=50, null=True, blank=True, verbose_name='状态描述')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '任务状态'
        verbose_name_plural = verbose_name


class TaskType(models.Model):
    """
    任务类型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='类型名称')
    index = models.IntegerField(verbose_name='类型序号')
    is_active = models.IntegerField(verbose_name='是否激活')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务类型'
        verbose_name_plural = verbose_name


class TaskPriority(models.Model):
    """
    任务优先级模型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='优先级名称')
    index = models.IntegerField(verbose_name='优先级序号')
    weight = models.FloatField(verbose_name='权重')

    is_active = models.IntegerField(verbose_name='是否激活', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务优先级'
        verbose_name_plural = verbose_name


class TaskQuality(models.Model):
    """
    任务品质要求表模型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='品质要求名称')
    index = models.IntegerField(verbose_name='品质要求序号')
    weight = models.FloatField(verbose_name='权重')

    is_active = models.IntegerField(verbose_name='是否激活', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务品质要求'
        verbose_name_plural = verbose_name


class TaskAssessment(models.Model):
    """
    任务评级
    """
    name = models.CharField(max_length=20, verbose_name='评级名称')
    index = models.IntegerField(verbose_name='评级序号')
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name='权重')

    is_active = models.IntegerField(verbose_name='是否激活')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务评级'
        verbose_name_plural = verbose_name


class TaskDesignType(models.Model):
    """
    任务设计方式
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, null=True, blank=True, verbose_name='任务类型标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='设计方式名称')
    index = models.IntegerField(verbose_name='设计方式序号')

    is_active = models.IntegerField(verbose_name='是否激活')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务设计方式'
        verbose_name_plural = verbose_name


class TaskStep(models.Model):
    """
    任务步骤表模型
    """
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name='公司标识', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='任务步骤名称')
    task_type = models.ForeignKey(TaskType, null=True, blank=True, verbose_name='任务类型标识', on_delete=models.CASCADE)
    task_design_type = models.ForeignKey(TaskDesignType, null=True, blank=True, verbose_name='任务设计方式标识', on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='步骤序号')

    is_active = models.IntegerField(verbose_name='是否激活')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务步骤'
        verbose_name_plural = verbose_name


class Salary(models.Model):
    """
    用户薪水
    """
    user = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='用户标识', on_delete=models.CASCADE)
    wage = models.FloatField(verbose_name='工资')
    is_active = models.IntegerField(verbose_name='是否激活', default=1)

    def __str__(self):
        return self.wage

    class Meta:
        verbose_name = '薪水'
        verbose_name_plural = verbose_name


class Skill(models.Model):
    """
    用户技能
    """
    user = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='用户标识', on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, null=True, blank=True, verbose_name='技能标识', on_delete=models.CASCADE)
    is_active = models.IntegerField(verbose_name='是否激活', default=1)

    class Meta:
        verbose_name = '用户技能'
        verbose_name_plural = verbose_name

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
