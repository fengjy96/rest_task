from rest_framework import serializers

from business.models.task import Task, TaskAllocateReason


class TaskSerializer(serializers.ModelSerializer):
    """
    任务：增删改查
    """

    class Meta:
        model = Task
        fields = '__all__'


class TaskListSerializer(serializers.ModelSerializer):
    """
    任务：查
    """

    label = serializers.CharField(source='get_label_display')

    class Meta:
        model = Task
        fields = '__all__'
        depth = 2


class TaskAllocateReasonSerializer(serializers.ModelSerializer):
    """
    任务分派原因：增删改查
    """

    class Meta:
        model = TaskAllocateReason
        fields = '__all__'
