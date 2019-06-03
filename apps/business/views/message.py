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

        queryset = self.filter_list_queryset(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def filter_list_queryset(self, request, queryset):
        """
        根据用户所属角色过滤查询集
        :param request:
        :param queryset:
        :return:
        """

        # 定义空的数据集
        emptyQuerySet = self.queryset.filter(status=999)
        queryset_project_auditor = emptyQuerySet
        queryset_project_manager = emptyQuerySet
        queryset_business_manager = emptyQuerySet

        # 获取当前用户 id
        user_id = request.user.id
        # 获取当前用户所属角色 id 列表
        user_role_ids = self.get_user_roles(user_id)

        # 如果当前用户拥有管理员权限，则不做特殊处理
        if 1 in user_role_ids:
            pass
        else:
            # 如果当前用户拥有项目审核员权限，则返回与该审核员关联的项目数据
            if 5 in user_role_ids:
                queryset_project_auditor = queryset.filter(auditor_id=user_id)
            # 如果当前用户拥有项目负责人权限，则返回与该项目负责人关联的项目数据
            if 7 in user_role_ids:
                queryset_project_manager = queryset.filter(receiver_id=user_id)
            # 如果当前用户拥有商务人员权限，则返回与该商务人员关联的项目数据
            if 8 in user_role_ids:
                queryset_business_manager = queryset.filter(sender_id=user_id)

            queryset = queryset_project_auditor | queryset_project_manager | queryset_business_manager

        return queryset

    def get_user_roles(self, user_id):
        if user_id is not None:
            user = UserProfile.objects.get(id=user_id)
            user_roles = user.roles.all()
            user_role_ids = set(map(lambda user_role: user_role.id, user_roles))
            return user_role_ids


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
