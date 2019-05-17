from rest_framework import serializers
from ..models import Business, DeviceInfo


class BusinessSerializer(serializers.ModelSerializer):
    """
    业务序列化
    """
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=DeviceInfo.objects.all(),
                                               source='deviceinfo_set')

    class Meta:
        model = Business
        fields = '__all__'
