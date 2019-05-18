from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from business.models.message import Message
from business.serializers.message_serializer import MessageSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import MessageFilter
from rest_framework.generics import ListAPIView


class MessageViewSet(ListAPIView):
    """
    消息：增删改查
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = MessageFilter
    ordering_fields = ('add_time',)

    def get_queryset(self):
        # 取状态数组
        status = self.request.data.get('status')
        status_list = status.split(',')

        return Message.objects.filter(status__in=status_list)
