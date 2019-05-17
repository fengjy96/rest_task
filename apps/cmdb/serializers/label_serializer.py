from rest_framework import serializers

from ..models import Label
from ..models import DeviceInfo


class LabelSerializer(serializers.ModelSerializer):
    """
    标签序列化
    """

    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=DeviceInfo.objects.all(),
                                               source='deviceinfo_set')

    class Meta:
        model = Label
        fields = '__all__'
