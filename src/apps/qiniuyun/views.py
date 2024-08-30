from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response
from rest_framework import status

# Create your views here.


"""
七牛云 python服务端SDK https://developer.qiniu.com/kodo/sdk/1242/python

"""

from qiniu import Auth, put_file, etag
import qiniu.config
import uuid
import hashlib


#需要填写你的 Access Key 和 Secret Key
access_key = '9ecHtV7xkF3UAkSaxLFLVqOqBCtboxJtkW0KPQhh'
secret_key = '_d1T2v_3DnjQTsRcAcJhIhzKG7ic1dSgYCW-ubW-'


bucket_name = 'pocket-bfu-miniprogram'


def uploadToken(filename):
    q = Auth(access_key, secret_key)
    policy = {
        # 'callbackUrl':'https://requestb.in/1c7q2d31',
        # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        # 'persistentOps':'imageView2/1/w/200/h/200'
        'mimeLimit': 'image/*'
    }
    key = hashlib.md5(str(uuid.uuid1()).encode("utf-8")).hexdigest() + str(filename)
    token = q.upload_token(bucket_name, key, 3600, policy)
    return key, token


class QiNiuView(APIView):
    throttle_classes = (UserRateThrottle,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            filename = request.GET['filename']
            dic = {}
            dic['key'], dic['uploadToken'] = uploadToken(filename)
            return Response(data=dic, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
