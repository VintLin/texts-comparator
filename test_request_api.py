# -*- coding: utf-8 -*-
"""
@date: 2020/4/30 2:49 下午
@desc：
    获取HTTP签名和发送HTTP请求Demo
    content-type: application/json
    python版本 > 3.0

"""
import uuid
import base64
import hmac
import time
import requests
import json
import sys

from hashlib import sha1
from urllib.parse import quote
from requests.exceptions import RequestException

# 判断python版本
if sys.version_info < (3, 0):
    raise RuntimeError('Python version must be > 3.0')


class ApplicationJsonRequest(object):
    def __init__(self, url, url_params, body_params, access_key_id, access_key_secret):

        # 设置请求头content-type
        self.headers = {'content-type': "application/json"}

        # 请求URL，请替换自己的真实地址
        self.url = url

        # 填写自己AK
        # 获取AK教程：https://openai.100tal.com/documents/article/page?fromWhichSys=admin&id=27
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

        # 根据接口要求，填写真实Body参数。key1、key2仅做举例
        self.body_params = body_params

        # 根据接口要求，填写真实URL参数。key1、key2仅做举例
        self.url_params = url_params

    @property
    def timestamp(self):
        # 获取当前时间（东8区）
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

    @staticmethod
    def url_format(params):
        """
        # 对params进行format
        # 对 params key 进行从小到大排序
        :param params: dict()
        :return:
        a=b&c=d
        """

        sorted_parameters = sorted(params.items(), key=lambda d: d[0], reverse=False)

        param_list = ["{}={}".format(key, value) for key, value in sorted_parameters]

        string_to_sign = '&'.join(param_list)
        return string_to_sign

    def _generate_signature(self, parameters, access_key_secret):

        # 计算证书签名
        string_to_sign = self.url_format(parameters)

        #  进行base64 encode
        secret = access_key_secret + "&"
        h = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), sha1)
        signature = base64.b64encode(h.digest()).strip()
        signature = str(signature, encoding="utf8")
        return signature

    def get_signature(self):

        self.url_params['access_key_id'] = self.access_key_id
        self.url_params['timestamp'] = self.timestamp

        # 组合URL和Body参数，并计算签名
        self.url_params['signature_nonce'] = str(uuid.uuid1())

        sign_param = {
            "request_body": json.dumps(self.body_params)
        }
        sign_param.update(self.url_params)

        signature = self._generate_signature(sign_param, self.access_key_secret)

        self.url_params['signature'] = quote(signature, 'utf-8')

    def run(self):
        # 生成签名
        self.get_signature()

        # 生成URL
        url = self.url + '?' + self.url_format(self.url_params)
        # 响应结果httpResponse
        try:
            response = requests.post(url, json=self.body_params, headers=self.headers)
            result = response.text
        except RequestException as e:
            result = str(e)
        print(result)
        return result

def main():
    url = "https://openai.100tal.com/aitext/ch-composition/text-correction"

    url_params = dict()
    # 根据接口要求，填写真实URL参数。key1、key2仅做举例
    body_params = {
        "user_id": "xxxx-xxxx-xxxx-xxxx",
        "user_name": "小明",
        "grade": 1,
        "min_text_length": 200,
        "max_text_length": 1200,
        "topic_type": 1,
        "answer_title": "放风筝",
        "answer_text": ['“草长莺飞二月天，拂堤杨柳醉春烟。”生机勃勃的春天来到了，这正是放风筝的好时节。 ', '郊外小朋友们正兴致勃勃地放着风筝'],
        "correction_type": 0,
        "max_score": 100,
        "requirement": 1,
        "knowledge": 1,
        "is_fragment": 1,
        "comment_type": 1,
        "spell_type": 0,
        "rotate_model": 1
    }

    access_key_id = "1250461020862812160"
    access_key_secret = "72a7b4e3edaf48839c0131369326a0bf"

    ApplicationJsonRequest(
            url=url, 
            access_key_id=access_key_id, 
            access_key_secret=access_key_secret,
            body_params=body_params, 
            url_params=url_params
        ).run()


if __name__ == '__main__':
    main()