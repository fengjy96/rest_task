from rest_framework import serializers
from business.models.reason import Reason


class ReasonsListSerializer(serializers.ModelSerializer):
    """
    原因：增删改查
    """
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

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

    class Meta:
        model = Reason
        fields = '__all__'
        depth = 1
