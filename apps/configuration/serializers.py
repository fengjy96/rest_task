from rest_framework import serializers
from configuration.models import TaskDesignType, TaskType, TaskQuality, TaskPriority, TaskAssessment, TaskStep, Skill, \
    Salary, ProjectStatus, TaskStatus, ReasonType


class ReasonTypeSerializer(serializers.ModelSerializer):
    """
    项目状态序列化
    """

    class Meta:
        model = ReasonType
        fields = '__all__'

class ProjectStatusSerializer(serializers.ModelSerializer):
    """
    项目状态序列化
    """

    class Meta:
        model = ProjectStatus
        fields = '__all__'


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    任务状态序列化
    """

    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskTypeSerializer(serializers.ModelSerializer):
    """
    任务类型序列化
    """

    class Meta:
        model = TaskType
        fields = '__all__'


class TaskDesignTypeSerializer(serializers.ModelSerializer):
    """
    任务设计类型序列化
    """

    class Meta:
        model = TaskDesignType
        fields = '__all__'


class TaskQualitySerializer(serializers.ModelSerializer):
    """
    任务质量序列化
    """

    class Meta:
        model = TaskQuality
        fields = '__all__'


class TaskPrioritySerializer(serializers.ModelSerializer):
    """
    任务优先级序列化
    """

    class Meta:
        model = TaskPriority
        fields = '__all__'


class TaskAssessmentSerializer(serializers.ModelSerializer):
    """
    任务评估序列化
    """

    class Meta:
        model = TaskAssessment
        fields = '__all__'


class TaskStepSerializer(serializers.ModelSerializer):
    """
    任务步骤序列化
    """

    class Meta:
        model = TaskStep
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    """
    薪水序列化
    """

    class Meta:
        model = Salary
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    """
    用户技能序列化
    """

    class Meta:
        model = Skill
        fields = '__all__'
