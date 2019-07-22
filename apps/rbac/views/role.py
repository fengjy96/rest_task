from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import CommonPagination, RbacPermission

from rbac.models import Role
from rbac.serializers.role_serializer import RoleListSerializer, RoleModifySerializer


class RoleViewSet(ModelViewSet):
    """
    角色管理：增删改查
    """

    perms_map = (
        {'*': 'admin'},
        {'*': 'role_all'},
        {'get': 'role_list'},
        {'post': 'role_create'},
        {'put': 'role_edit'},
        {'delete': 'role_delete'}
    )
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer
    pagination_class = CommonPagination
    permission_classes = (RbacPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleModifySerializer
