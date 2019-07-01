from rest_framework import serializers
from configuration.models.task_conf import TaskDesignType, TaskType, TaskQuality, TaskPriority, TaskAssessment, \
    TaskStep, TaskStatus
from configuration.models.project_conf import ProjectStatus, Fee
from configuration.models.reason_conf import ReasonType


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


class TaskDesignTypeListSerializer(serializers.ModelSerializer):
    """
    任务设计类型序列化
    """

    class Meta:
        model = TaskDesignType
        fields = '__all__'
        depth = 1


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


class TaskStepListSerializer(serializers.ModelSerializer):
    """
    任务步骤列表序列化
    """

    class Meta:
        model = TaskStep
        fields = '__all__'
        depth = 1


class TaskStepSerializer(serializers.ModelSerializer):
    """
    任务步骤序列化
    """

    class Meta:
        model = TaskStep
        fields = '__all__'


class FeeSerializer(serializers.ModelSerializer):
    """
    费用序列化
    """

    class Meta:
        model = Fee
        fields = '__all__'
