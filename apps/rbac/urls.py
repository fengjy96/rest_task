from django.urls import path, include
from rest_framework import routers

from rbac.views import user, organization, menu, role, permission
from cmdb.views import dict

router = routers.SimpleRouter()
# 用户相关
router.register(r'users', user.UserViewSet, basename="users")
# 组织相关
router.register(r'organizations', organization.OrganizationViewSet, basename="organization")
# 菜单相关
router.register(r'menus', menu.MenuViewSet, basename="menus")
# 权限相关
router.register(r'permissions', permission.PermissionViewSet, basename="permissions")
# 角色相关
router.register(r'roles', role.RoleViewSet, basename="roles")
# 字典相关
router.register(r'dicts', dict.DictViewSet, basename="dicts")

urlpatterns = [
    path(r'api/', include(router.urls)),
    # 登录
    path(r'auth/login/', user.UserAuthView.as_view()),
    # 获取用户信息
    path(r'auth/info/', user.UserInfoView.as_view(), name='user_info'),
    # 构建用户菜单
    path(r'auth/build/menus/', user.UserBuildMenuView.as_view(), name='build_menus'),
    # 获取组织树
    path(r'api/organization/tree/', organization.OrganizationTreeView.as_view(), name='organizations_tree'),
    # 获取组织用户树
    path(r'api/organization/user/tree/', organization.OrganizationUserTreeView.as_view(),
         name='organization_user_tree'),
    # 获取菜单树
    path(r'api/menu/tree/', menu.MenuTreeView.as_view(), name='menus_tree'),
    # 获取权限树
    path(r'api/permission/tree/', permission.PermissionTreeView.as_view(), name='permissions_tree'),
    # 获取用户列表
    path(r'api/user/list/', user.UserListView.as_view(), name='user_list'),
    # 修改用户头像
    path(r'api/user/avatar/upload', user.UserAvatarUploadView.as_view(), name='user_avatar_upload'),
]
