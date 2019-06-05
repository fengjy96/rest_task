from rest_framework import serializers

from business.models.files import Files


class FilesSerializer(serializers.ModelSerializer):
    """
    文件：增删改查
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
