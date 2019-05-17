from rest_framework import serializers

from business.models.project import Project, ProjectFee, ProjectRejectReason, ProjectCost
from business.models.task import Task, TaskAllocateReason
from business.models.step import Step, StepRejectReason
from business.models.message import Message
from business.models.files import Files
from rbac.models import UserProfile


class ProjectReceiverListSerializer(serializers.ModelSerializer):
    """
    项目：查
    """

    class Meta:
        model = UserProfile
        fields = ['id', 'name']


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目：增删改查
    """

    class Meta:
        model = Project
        fields = '__all__'
        depth = 1


class ProjectListSerializer(serializers.ModelSerializer):
    """
    项目：查
    """

    class Meta:
        model = Project
        fields = '__all__'
        depth = 1


class ProjectFeeSerializer(serializers.ModelSerializer):
    """
    项目费用：增删改查
    """

    class Meta:
        model = ProjectFee
        fields = '__all__'


class ProjectRejectReasonSerializer(serializers.ModelSerializer):
    """
    项目拒绝原因：增删改查
    """

    class Meta:
        model = ProjectRejectReason
        fields = '__all__'


class ProjectCostSerializer(serializers.ModelSerializer):
    """
    项目成本：增删改查
    """

    class Meta:
        model = ProjectCost
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """
    任务：增删改查
    """

    class Meta:
        model = Task
        fields = '__all__'
        depth = 1


class TaskListSerializer(serializers.ModelSerializer):
    """
    项目：查
    """

    class Meta:
        model = Task
        fields = '__all__'
        depth = 1


class TaskAllocateReasonSerializer(serializers.ModelSerializer):
    """
    任务分派原因：增删改查
    """

    class Meta:
        model = TaskAllocateReason
        fields = '__all__'


class StepSerializer(serializers.ModelSerializer):
    """
    任务步骤：增删改查
    """

    class Meta:
        model = Step
        fields = '__all__'
        depth = 1


class StepListSerializer(serializers.ModelSerializer):
    """
    项目：查
    """

    class Meta:
        model = Step
        fields = '__all__'
        depth = 1


class StepRejectReasonSerializer(serializers.ModelSerializer):
    """
    任务步骤拒绝原因：增删改查
    """

    class Meta:
        model = StepRejectReason
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """
    消息：增删改查
    """

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1


class FilesSerializer(serializers.ModelSerializer):
    """
    消息：增删改查
    """

    class Meta:
        model = Files
        fields = '__all__'


class FilesListSerializer(serializers.ModelSerializer):
    """
    消息：增删改查
    """

    class Meta:
        model = Files
        fields = '__all__'
        depth = 1
