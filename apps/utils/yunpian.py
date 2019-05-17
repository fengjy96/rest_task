import json

import requests


APIKEY = '云片网的 API 密钥'


class YunPian:
    def __init__(self, api_key):
        ## 云片网的 api 密钥
        self.api_key = api_key
        ## 单次发送的 URL
        self.single_send_url = 'https://sms.yunpain.com/v2/sys/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            ## 注意 text 内容必须要与后台已申请过签名并审核通过的模版保持一致
            'text': '【米开任务管理系统】您的验证码是 {code}。如非本人操作，请忽略本短信。'.format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        ret_dict = json.loads(response.text)
        return ret_dict


if __name__ == '__main__':
    yun_pian = YunPian(APIKEY)
    yun_pian.send_sms('2019', '手机号')