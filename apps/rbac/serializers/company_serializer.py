from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rbac.models import Company, AuthCode


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    公司详情序列化
    """

    class Meta:
        model = Company
        fields = ['id', 'name', 'account', 'mobile', 'avatar']


class CompanyRegisterSerializer(serializers.ModelSerializer):
    """
    公司注册序列化
    """
    code = serializers.CharField(
        label='验证码',
        required=True,
        write_only=True,
        allow_blank=False,
        min_length=4,
        max_length=4,
        help_text='验证码',
        # 自定义错误消息提示的格式
        error_messages={
            'blank': '请输入验证码',
            'required': '请输入验证码',
            'max_length': '验证码格式错误',
            'min_length': '验证码格式错误',
        },
    )
    name = serializers.CharField(
        label='公司名',
        help_text='公司名',
        required=True,
        allow_blank=False,
        # 利用 drf 中的 validators 验证 name 是否唯一
        validators=[UniqueValidator(queryset=Company.objects.all(), message='公司名已经存在')],
    )
    password = serializers.CharField(
        label='密码',
        style={'input_type': 'password'},
        help_text='密码',
        write_only=True,
    )

    def create(self, validated_data):
        """
        创建一个公司
        :param validated_data:
        :return:
        """
        company = Company.objects.create(**validated_data)
        password = make_password(validated_data['password'])
        company.password = password
        company._password = validated_data['password']
        company.save()
        return company

    def validate_code(self, code):
        """
        验证验证码（函数名必须为 validate_ + 字段名）
        :param code: 验证码
        :return:
        """
        # 验证码在数据库中是否存在，用户从前端 post 过来的值都会放入 initial_data 中，排序（最新一条）
        verify_records = AuthCode.objects.filter(mobile=self.initial_data['mobile']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]

            # 判断验证码是否过期（有效期为五分钟）
            five_minutes_age = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_age > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            # 判断验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        可以作用于所有字段
        不加字段名的验证器作用于所有字段之上
        :param attrs:
        :return:
        """
        try:
            del attrs['code']
            pass
        except:
            pass
        return attrs

    class Meta:
        model = Company
        fields = ('name', 'code', 'account', 'mobile', 'password', 'avatar')
