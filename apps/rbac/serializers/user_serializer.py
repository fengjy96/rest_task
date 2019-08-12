import re

from rest_framework import serializers

from rbac.models import UserProfile


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化
    """

    roles = serializers.SerializerMethodField()
    superior = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    def get_superior(self, obj):
        return {
            'id': obj.superior.id,
            'name': obj.superior.name,
            'username': obj.superior.username
        } if obj.superior else obj.superior

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles', 'skills', 'base_salary']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    """
    用户编辑序列化
    """

    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles', 'skills', 'base_salary']

    def validate_mobile(self, mobile):
        """
        校验手机号是否合法
        :param mobile:
        :return:
        """
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


class UserCreateSerializer(serializers.ModelSerializer):
    """
    创建用户序列化
    """

    username = serializers.CharField(required=True, allow_blank=False)
    mobile = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'department', 'position', 'is_active', 'roles',
                  'password', 'skills', 'base_salary', 'superior']

    def validate_username(self, username):
        """
        校验用户名是否存在
        :param username:
        :return:
        """
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        """
        校验手机号是否合法、是否已被注册
        :param mobile:
        :return:
        """
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile


class UserInfoListSerializer(serializers.ModelSerializer):
    """
    公共 users 信息
    """

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'mobile', 'email', 'position', 'skills')
