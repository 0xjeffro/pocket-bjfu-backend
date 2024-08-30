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

from .utils import get_days_of_week, get_current_week
from interface.jwxt import interface_kcb

# Create your views here.


class KeChengBiao(APIView):
    throttle_classes = (UserRateThrottle,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request_user = request.user
            user = UserProfile.objects.get(openId=request_user.openId)
            current_week = request.GET.get('currentWeek', None)
            if current_week == 'default':
                current_week = get_current_week()

            data = dict()
            data['weekDate'] = get_days_of_week(current_week)
            data['kcb'] = interface_kcb(user.xh, user.pwd, current_week)['kcb']
            data['currentWeek'] = current_week
            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)