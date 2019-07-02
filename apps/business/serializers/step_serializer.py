from rest_framework import serializers

from business.models.step import Step, StepRejectReason


class StepListSerializer(serializers.ModelSerializer):
    """
    任务步骤：查
    """

    label = serializers.CharField(source='get_label_display')

    class Meta:
        model = Step
        fields = '__all__'
        depth = 2


class StepSerializer(serializers.ModelSerializer):
    """
    任务步骤：增删改查
    """

    class Meta:
        model = Step
        fields = '__all__'


class StepRejectReasonSerializer(serializers.ModelSerializer):
    """
    任务步骤拒绝原因：增删改查
    """

    class Meta:
        model = StepRejectReason
        fields = '__all__'
