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

from apps.users.models import UserProfile

from apps.kechengbiao.utils import get_current_week
from .utils import get_current_jc, get_day_of_week
from interface.jwxt import interface_kjs

from django.conf import settings

# Create your views here.


class KongJiaoShi(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request_user = request.user
            user = UserProfile.objects.get(openId=request_user.openId)
            type = request.GET.get('type')  # default: 默认当前时间， request: 根据请求参数返回
            week = request.GET.get('week', None)  # 第几周，1，2，3，..., 19
            day = request.GET.get('day', None)  # 星期几，1，2，3，4，5，6，7
            jc = request.GET.get('jc', None)
            """
                节次，0-5
                0：*-2节
                1：3-4节
                2：5节
                3：6-7节
                4：8-9节
                5：10-*节课
            """
            jxl = request.GET.get('jxl', None)
            """
                教学楼：
                0：全部， 1，一教 2，二教 3，学研
            """

            if type == 'request':
                data = {}
                value = [int(week) - 1, int(day) - 1, jc, jxl]
                kjs = interface_kjs(xh=user.xh, pwd=user.pwd, xnxqh=settings.XNXQID, zc=week, xq=day, _jc=jc, jxl=jxl)
                data['value'] = value
                data['kjs'] = kjs
                return Response(status=status.HTTP_200_OK, data=data)
            else:
                data = {}
                value = [get_current_week() - 1, get_day_of_week() - 1, get_current_jc(), 0]
                kjs = interface_kjs(xh=user.xh, pwd=user.pwd, xnxqh=settings.XNXQID, zc=get_current_week(),
                                    xq=get_day_of_week(), _jc=get_current_jc(), jxl=0)
                data['value'] = value
                data['kjs'] = kjs
                return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)