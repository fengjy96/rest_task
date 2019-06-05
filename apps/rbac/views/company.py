from rest_framework import mixins, viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rbac.serializers.company_serializer import CompanyDetailSerializer, CompanyRegisterSerializer
from rbac.models import Company


class CompanyViewSet(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    公司管理
    """
    # serializer_class = CompanyRegisterSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Company.objects.all()
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        elif self.action == 'create':
            return CompanyRegisterSerializer
        return CompanyDetailSerializer

    def get_permissions(self):
        # 检索公司，需要有权限
        if self.action == 'retrieve':
            # return []
            return [permissions.IsAuthenticated()]
        # 创建公司，不需要权限
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.perform_create(serializer)

        ret_dict = serializer.validated_data
        # payload = jwt_payload_handler(company)
        # ret_dict['token'] = jwt_encode_handler(payload)
        ret_dict['name'] = company.name

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.company

    def perform_create(self, serializer):
        return serializer.save()
