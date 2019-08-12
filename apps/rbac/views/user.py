"""
基于 RBAC 的用户权限管理：用户视图
"""

import os
import time

from PIL import Image

from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend

import jwt
from operator import itemgetter

from rest_xops import settings
from rest_xops.settings import SECRET_KEY
from rest_xops.basic import XopsResponse
from rest_xops.code import *

from deployment.models import Project
from cmdb.models import ConnectionInfo
from rbac.models import UserProfile, Menu
from rbac.serializers.user_serializer import (UserListSerializer, UserCreateSerializer,
                                              UserModifySerializer, UserInfoListSerializer)
from rbac.serializers.menu_serializer import MenuSerializer

from common.custom import CommonPagination, RbacPermission

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    """
    处理用户登录，返回用户登录成功后的 token
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            # 用户登录成功后，返回生成好的 token 给前端（token 是动态生成的，每次用户登录成功后，值都是不同的）
            return XopsResponse({'token': jwt.encode(payload, SECRET_KEY)}, status=OK)
        else:
            return XopsResponse('用户名或密码错误!', status=BAD)


class UserInfoView(APIView):
    """
    获取当前用户相关信息
    """

    def get(self, request):
        if request.user.id is not None:
            # 根据当前用户所拥有的角色，返回相应的权限列表
            perms = self.get_permission_from_role(request)
            skills = self.get_skills(request)
            data = {
                'id': request.user.id,
                'username': request.user.username,
                'avatar': request._request._current_scheme_host + '/media/' + str(request.user.image),
                'email': request.user.email,
                'is_active': request.user.is_active,
                'createTime': request.user.date_joined,
                'roles': perms,
                'skills': skills,
            }
            # 如果存在用户 id 则返回当前用户的相关数据给前端（用户 id，用户名，头像，邮箱，...）
            return XopsResponse(data, status=OK)
        else:
            return XopsResponse('请登录后访问!', status=FORBIDDEN)

    @classmethod
    def get_permission_from_role(self, request):
        try:
            if request.user:
                # 存储权限列表
                perms_list = []
                # 查询与当前用户关联的角色所拥有的权限
                for item in request.user.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                # 返回权限列表，如 ['admin', 'user_all', 'user_edit', ...]
                return perms_list
        except AttributeError:
            return None

    @classmethod
    def get_skills(self, request):
        try:
            if request.user:
                # 存储权限列表
                skill_list = []
                for item in request.user.skills.values('id', 'name'):
                    skill_list.append(item)
                return skill_list
            else:
                return []
        except AttributeError:
            return None


class UserBuildMenuView(APIView):
    """
    获取当前用户所拥有的权限，构建菜单，返回给前端
    """

    def get(self, request):
        if request.user.id is not None:
            # 获取当前用户所拥有的所有菜单数据
            menu_data = self.get_all_menus(request)
            return XopsResponse(menu_data, status=OK)
        else:
            return XopsResponse('请登录后访问!', status=FORBIDDEN)

    def get_all_menus(self, request):
        """
        获取当前用户所拥有的所有菜单
        :param request: 当前用户请求
        :return: 当前用户所拥有的菜单数据
        """

        # 根据当前用户所属的角色，获取相应的权限列表，如 ['admin', 'user_all', 'user_edit', ...]
        perms = UserInfoView.get_permission_from_role(request)

        tree_data = []
        # 如果 'admin' 在权限列表中，或当前用户是超级管理员，则获取所有菜单数据
        if 'admin' in perms or request.user.is_superuser:
            tree_dict = self.get_all_menu_dict()
        # 否则，根据当前用户所属的角色获取菜单数据
        else:
            tree_dict = self.get_menu_from_role(request)

        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                # parent = tree_dict[pid]
                parent = tree_dict.get(pid, -1)
                if parent == -1:
                    continue
                parent.setdefault('redirect', 'noredirect')
                parent.setdefault('alwaysShow', True)
                parent.setdefault('children', []).append(tree_dict[i])
                parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
            else:
                tree_data.append(tree_dict[i])
        return tree_data

    def get_menu_from_role(self, request):
        """
        根据当前用户所属的角色获取菜单数据
        :param request:
        :return:
        """
        if request.user:
            menu_dict = {}
            menus = request.user.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__pid'] is None:
                    if item['menus__is_frame']:
                        # 判断是否外部链接
                        top_menu = {
                            'id': item['menus__id'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'children': [{
                                'path': item['menus__path'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                }
                            }],
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        top_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': '/' + (item['menus__path'] or ''),
                            'redirect': 'noredirect',
                            'component': 'Layout',
                            'alwaysShow': True,
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon']
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'children': []
                        }
                    menu_dict[item['menus__id']] = top_menu
                else:
                    if item['menus__is_frame']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    elif item['menus__is_show']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'noCache': True,
                            },
                            'hidden': True,
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        """
        获取所有菜单数据，重组结构
        :return:
        """
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                # 如果是外部菜单
                if item['is_frame']:
                    # 判断是否是外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'Layout',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                # 否则是内部菜单
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'redirect': 'noredirect',
                        'component': 'Layout',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'Layout',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict


class UserViewSet(ModelViewSet):
    """
    用户管理：增删改查
    """

    # 请求方法与权限映射
    perms_map = (
        {'*': 'admin'},
        {'*': 'user_all'},
        {'get': 'user_list'},
        {'post': 'user_create'},
        {'put': 'user_edit'},
        {'delete': 'user_delete'}
    )
    queryset = UserProfile.objects.all()
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        """
        根据请求类型动态变更 serializer
        :return:
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        self.before_create(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 自定义返回响应数据
        return XopsResponse(serializer.data, status=CREATED, headers=headers)

    def before_create(self, request):
        """
        创建用户时指定默认密码为 123456
        :param request:
        :return:
        """
        request.data['password'] = '123456'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.before_destroy(request, kwargs)

        self.perform_destroy(instance)
        return XopsResponse(status=NO_CONTENT)

    def before_destroy(self, request, kwargs):
        """
        删除用户时，同时删除其他与该用户关联的表
        :param request:
        :param kwargs:
        :return:
        """
        id = str(kwargs['pk'])
        projects = Project.objects.filter(
            Q(user_id__icontains=id + ',') | Q(user_id__in=id) | Q(user_id__endswith=',' + id)
        ).values()
        if projects:
            for project in projects:
                user_id = project['user_id'].split(',')
                user_id.remove(id)
                user_id = ','.join(user_id)
                Project.objects.filter(id=project['id']).update(user_id=user_id)
        ConnectionInfo.objects.filter(uid_id=id).delete()

    @action(
        methods=['post'], detail=True, permission_classes=[IsAuthenticated],
        url_path='change-passwd', url_name='change-passwd'
    )
    def set_password(self, request, pk=None):
        perms = UserInfoView.get_permission_from_role(request)
        user = UserProfile.objects.get(id=pk)
        if 'admin' in perms or 'user_all' in perms or request.user.is_superuser:
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return XopsResponse('密码修改成功!')
            else:
                return XopsResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
        else:
            old_password = request.data['old_password']
            if check_password(old_password, user.password):
                new_password1 = request.data['new_password1']
                new_password2 = request.data['new_password2']
                if new_password1 == new_password2:
                    user.set_password(new_password2)
                    user.save()
                    return XopsResponse('密码修改成功!')
                else:
                    return XopsResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
            else:
                return XopsResponse('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    获取用户列表
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class UserAvatarUploadView(APIView):
    """
    修改用户头像
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # 原始文件名
            raw_file_name = request.FILES['file'].name
            # 文件的后缀
            suffix = os.path.splitext(raw_file_name)[-1][1:]
            # 时间戳作为头像的名称
            name = str(time.time()).split('.')[0].strip()
            # 图片名称
            avatar_name = 'avatar/{}/{}.{}'.format(request.user.username, name, suffix)
            # pillow 打开图片，保存副本
            avatar = Image.open(request.data['file'])
            # 生成缩略图
            thumb = self.make_thumb(avatar)
            # 判断文件的父文件是否存在，不存在则创建
            if not os.path.exists('media/avatar/' + request.user.username):
                os.makedirs('media/avatar/' + request.user.username)

            # 文件保存的具体路径（只保存缩略图）
            avatar_file_path = os.path.join(settings.MEDIA_ROOT, avatar_name).replace('\\', '/')
            thumb.save(avatar_file_path)
            # 将保存的路径更新到数据库
            request.user.image = avatar_name.replace('\\', '/')
            request.user.save()
            # 返回结果
            return XopsResponse(status=OK, data={'avatar': avatar_name})
        except Exception as e:
            return XopsResponse(status=BAD)

    def make_thumb(self, img, size=150):
        width, height = img.size
        if height > size:
            delta = height / size
            width = int(width / delta)
            img.thumbnail((width, height), Image.ANTIALIAS)
        return img
