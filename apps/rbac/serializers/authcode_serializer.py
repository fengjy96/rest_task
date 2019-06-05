import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model

from rest_framework import serializers

from ..models import AuthCode


User = get_user_model()

# 手机号码的正则表达式
REGEXP_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'


class AuthCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, help_text='手机号')

    def validate_mobile(self, mobile):
        """
        验证手机号码（函数名必须为 validate_ + 字段名）
        :param mobile:
        :return:
        """
        # 验证手机号码是否已注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('该手机号码已经被注册')

        # 验证手机号码是否合法
        if not re.match(REGEXP_MOBILE, mobile):
            raise serializers.ValidationError('手机号码格式错误')

        # 验证发送频率
        one_minute_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if AuthCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile).count():
            raise serializers.ValidationError('请一分钟后再次发送')

        return mobile
