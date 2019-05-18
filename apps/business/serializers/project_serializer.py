from rest_framework import serializers

from business.models.project import Project, ProjectFee, ProjectRejectReason, ProjectCost
from rbac.models import UserProfile


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目：增删改查
    """

    class Meta:
        model = Project
        fields = '__all__'
        depth = 1


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    项目创建
    """

    class Meta:
        model = Project
        fields = '__all__'


class ProjectRejectReasonSerializer(serializers.ModelSerializer):
    """
    项目拒绝原因：增删改查
    """

    class Meta:
        model = ProjectRejectReason
        fields = '__all__'


class ProjectFeeSerializer(serializers.ModelSerializer):
    """
    项目费用：增删改查
    """

    class Meta:
        model = ProjectFee
        fields = '__all__'


class ProjectCostSerializer(serializers.ModelSerializer):
    """
    项目成本：增删改查
    """

    class Meta:
        model = ProjectCost
        fields = '__all__'


class ProjectReceiverListSerializer(serializers.ModelSerializer):
    """
    项目：查
    """

    class Meta:
        model = UserProfile
        fields = ['id', 'name']
