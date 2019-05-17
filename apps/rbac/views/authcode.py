from random import choice

from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from ..serializers.authcode_serializer import AuthCodeSerializer
from ..models import AuthCode
from utils.yunpian import YunPian


APIKEY = '云片网的 API 密钥'


class AuthCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    短信验证码视图集合
    """
    serializer_class = AuthCodeSerializer

    def generate_code(self):
        """
        随机生成四位数字的验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # 有效性验证失败会直接抛出异常（400 页面）
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        try:
            yun_pian = YunPian(APIKEY)
            sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        except:
            ## TODO: 测试环境，待删除
            sms_status = {}
            sms_status['code'] = 0

        if sms_status['code'] != 0:
            return Response({'mobile': sms_status['msg']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = AuthCode(code=code, mobile=mobile)
            code_record.save()
            return Response({'mobile': mobile}, status=status.HTTP_201_CREATED)
