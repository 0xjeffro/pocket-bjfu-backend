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

from apps.users.models import UserProfile

from interface.jwxt import interface_cj, interface_pm


class ChengJi(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request_user = request.user
            model_user = UserProfile.objects.get(openId=request_user.openId)
            xnxq = request.GET.get('xnxq')
            data = interface_cj(model_user.xh, model_user.pwd, xnxq)
            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)


class PaiMing(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request_user = request.user
            model_user = UserProfile.objects.get(openId=request_user.openId)
            data = interface_pm(model_user.xh, model_user.pwd)

            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)