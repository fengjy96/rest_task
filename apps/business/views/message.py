from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from business.models.message import Message
from business.serializers.message_serializer import MessageListSerializer, MessageSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from business.filters import MessageFilter
from common.custom import CommonPagination

from rbac.models import UserProfile
from utils.basic import MykeyResponse


class MessageViewSet(ModelViewSet):
    """
    消息：增删改查
    """
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    # 指定授权类
    permission_classes = (IsAuthenticated,)
    # 指定认证类
    authentication_classes = (JSONWebTokenAuthentication,)
    # 指定分页类
    pagination_class = CommonPagination

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # 指定筛选类
    filter_class = MessageFilter
    ordering = ('-add_time',)
    ordering_fields = ('-add_time',)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'list':
            return MessageListSerializer
        return MessageSerializer

    def get_queryset(self):
        # 取状态数组
        status = self.request.query_params.get('status', '')
        status_list = status.split(',')

        queryset = Message.objects.filter(status__in=status_list)

        for message in queryset:
            if message.status == 0:
                message.status = 1
                message.save()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        receiver_id = request.user.id

        queryset = queryset.filter(receiver_id=receiver_id)

        # queryset = self.filter_list_queryset(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageUpdateViewSet(APIView):
    """
    消息状态更新
    """

    def post(self, request, format=None):
        try:
            message_ids = request.data
            for message_id in message_ids:
                # 更新消息状态为已读
                self.update_message(message_id, 2)

        except Exception as e:
            msg = e.args if e else '请求失败'
            return MykeyResponse(status=status.HTTP_400_BAD_REQUEST, msg=msg)
        return MykeyResponse(status=status.HTTP_200_OK, msg='请求成功')

    def update_message(self, message_id, status):
        """
        更新单条消息状态
        :param message_id:
        :param status:
        :return:
        """
        if message_id is not None:
            message = Message.objects.get(id=message_id)
            if message:
                message.status = status
                message.save()
