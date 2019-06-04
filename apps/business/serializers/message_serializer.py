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
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()

    def get_sender(self, obj):
        if obj.sender:
            return {
                'id': obj.sender.id,
                'name': obj.sender.name,
            }

    def get_receiver(self, obj):
        if obj.receiver:
            return {
                'id': obj.receiver.id,
                'name': obj.receiver.name,
            }

    def get_menu(self, obj):
        if obj.menu:
            return {
                'id': obj.menu.id,
                'name': obj.menu.name,
                'component': obj.menu.component,
            }

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1