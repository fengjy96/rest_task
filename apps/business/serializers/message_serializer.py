from rest_framework import serializers

from business.models.message import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    消息：增删改查
    """

    class Meta:
        model = Message
        fields = '__all__'


class MessageListSerializer(serializers.ModelSerializer):
    """
    消息：查
    """

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1