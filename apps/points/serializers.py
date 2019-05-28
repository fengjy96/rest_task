from rest_framework import serializers

from points.models.points import Points
from points.models.projectpoints import ProjectPoints
from points.models.pointsdetail import PointsDetail


class PointsSerializer(serializers.ModelSerializer):
    """
    用户积分：增删改查
    """

    class Meta:
        model = Points
        fields = '__all__'

class ProjectPointsSerializer(serializers.ModelSerializer):
    """
    项目积分：增删改查
    """

    class Meta:
        model = ProjectPoints
        fields = '__all__'

class PointsDetailSerializer(serializers.ModelSerializer):
    """
    积分明细：增删改查
    """

    class Meta:
        model = PointsDetail
        fields = '__all__'