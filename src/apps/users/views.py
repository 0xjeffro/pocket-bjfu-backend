from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rest_framework.views import APIView

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status

import requests
from rest_framework_jwt.settings import api_settings

from django.conf import settings

from .models import UserProfile

from interface import jwxt, zsb, idcard

from django.utils import timezone

from utils.FeiShuMessage import send_feishu_msg
from utils.permission import is_black_user

# Create your views here.


class WxLogin(APIView):
    """
    POST:
        1. 接收客户端wx.login()获得的code
        2. 用code, AppID, AppSecret请求微信服务器，获得用户的openid
        3. 如果openid没在用户表内，create
        4. 生成一个JWT
        5. 返回 JWT
    """
    throttle_classes = (AnonRateThrottle, )
    permission_classes = (AllowAny, )

    def post(self, request):
        print('123')
        data = request.data
        try:
            code = data['code']
            req = requests.get(url='https://api.weixin.qq.com/sns/jscode2session?' +
                                   'appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(settings.APPID, settings.APPSECRET, code))
            openid = req.json()['openid']

            if UserProfile.objects.filter(openId=openid).count() == 0:
                UserProfile.objects.create(openId=openid, username=openid)

            user = UserProfile.objects.get(openId=openid)

            user.last_active = timezone.now()
            user.save()

            if is_black_user(user):
                send_feishu_msg('黑名单用户尝试获取Token，已被拒绝，姓名：{0} 学号：{1} openId: {2}'.format(user.realName, user.xh, user.openId))
                raise Exception('黑名单用户')

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response(status=status.HTTP_200_OK, data={'JWT': token})
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


class GetAccessToken(APIView):
    """
        用于给其他服务生成调用接口的jwt

        其他服务通过GET方法并携带参数serviceId,
        如果serviceId在services中，返回一个JWT
    """
    permission_classes = (AllowAny,)
    services = ['jwcnews98769863']

    def get(self, request):
        try:
            service_id = request.GET.get('serviceId')
            if service_id in self.services:
                user = UserProfile.objects.get(username='qujintao')

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                return Response(status=status.HTTP_200_OK, data={'JWT': token})
            else:
                return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


class JwLogin(APIView):
    """
    POST:
        1. 接收客户端传来的用户名和密码
        2. 执行验证逻辑，验证用户名和密码是否正确
            - 正确：
                1. 存储学号密码
                2. 返回登录成功状态
            - 错误：
                返回登录失败状态
    """
    throttle_classes = (UserRateThrottle, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request):
        request_user = request.user

        user = UserProfile.objects.get(openId=request_user.openId)

        data = request.data
        try:
            xh = data['xh']
            pwd = data['pwd']

            result = jwxt.interface_verify(xh, pwd)
            if result['success'] is True:
                user = UserProfile.objects.get(openId=request_user.openId)
                user.xh = xh
                user.pwd = pwd
                user.realName = result['name']
                user.academy = result['academy']
                user.verifyType = '1'
                user.save()
                if is_black_user(user):
                    send_feishu_msg(
                        '黑名单用户尝试教务登录，已被拒绝，姓名：{0} 学号：{1} openId: {2}'.format(user.realName, user.xh, user.openId))
                    raise Exception('黑名单用户')

                send_feishu_msg('姓名：{0} 学号：{1} 学院：{2} 教务验证成功！'.format(user.realName, user.xh, user.academy))

                return Response(status=status.HTTP_200_OK, data={
                    'success': 0,
                    'xh': xh,
                    'pwd': pwd,
                    'verifyType': '1'
                })
            else:
                send_feishu_msg('学号：{0} 密码：{1} 教务验证失败！'.format(xh, pwd))
                return Response(status=status.HTTP_200_OK, data={
                    'success': 1
                })

        except Exception as e:
            send_feishu_msg('教务验证出错！学号：{0} 密码：{1} 错误信息：{2}'.format(data['xh'], data['pwd'], str(e)))
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


class ZsbLogin(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request):
        request_user = request.user

        user = UserProfile.objects.get(openId=request_user.openId)
        if is_black_user(user):
            send_feishu_msg('黑名单用户尝试招生办登录，已被拒绝，姓名：{0} 学号：{1} openId: {2}'.format(user.realName, user.xh, user.openId))
            raise Exception('黑名单用户')

        data = request.data
        realName = data['studentName']
        ksh = data['ksh']
        sfzh = data['sfzh']
        try:
            zsb_result = zsb.query_admission_info(ksh=ksh, sfzh=sfzh)
            idcard_result = idcard.user_idcard_name_validate(name=realName, idcard=sfzh)

            result = zsb_result or idcard_result

            if result is True:  # 验证成功
                user = UserProfile.objects.get(openId=request_user.openId)

                if user.verifyType != '0' and user.verifyType != '2':
                    send_feishu_msg('【新绿验证失败】姓名：{0} 考生号：{1} 身份证号：{2} INFO: 装嫩'.format(realName, ksh, sfzh))
                    return Response(status=status.HTTP_200_OK, data={
                        'success': 1
                    })

                user.realName = realName
                user.ksh = ksh
                user.sfzh = sfzh

                user.xh = '210000000'  # 新绿学号初始化为21

                user.verifyType = '2'
                user.save()

                send_feishu_msg('【新绿验证（{0}）成功】姓名：{1}'.format('zsb' if zsb_result is True else 'id_card', user.realName))

                return Response(status=status.HTTP_200_OK, data={
                    'success': 0,
                    'verifyType': '2'
                })
            else:
                send_feishu_msg('【新绿验证失败】姓名：{0} 考生号：{1} 身份证号：{2}'.format(realName, ksh, sfzh))
                return Response(status=status.HTTP_200_OK, data={
                    'success': 1
                })
        except Exception as e:
            send_feishu_msg('【教务验证异常】姓名：{0} 考生号：{1} 身份证号：{2} ERROR: {3}'.format(realName, ksh, sfzh, str(e)))
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request):
        user = request.user
        if is_black_user(user):
            send_feishu_msg('黑名单用户尝试获取用户类型失败，姓名：{0} 学号：{1} openId：{2}'.format(user.realName, user.xh, user.openId))
            raise Exception('黑名单用户')

        try:
            return Response(status=status.HTTP_200_OK, data={
                'xh': user.xh,
                'pwd': user.pwd,
                'verifyType': user.verifyType
            })
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class JWTBackend(ModelBackend):
    """
    自定义jwt用户验证, 只验证是否存在openId与传入的username相同

    注意：虽然注册时username=unionId但这里验证unionId是否等于username,
         因为后台管理staff=True的人员没有unionid,这保证了不会爆破username导致入侵。
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(openId=username)
            if user is not None:
                return user
        except Exception as e:
            return None
