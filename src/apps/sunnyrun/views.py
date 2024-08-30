from django.shortcuts import render

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from apps.users.models import UserProfile
from interface.sunnyrun import interface_sunny_run
from django.conf import settings

# Create your views here.


class SunnyRun(APIView):
    throttle_classes = (UserRateThrottle, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            request_user = request.user
            user = UserProfile.objects.get(openId=request_user.openId)
            xh = user.xh
            data = interface_sunny_run(xh)
            d_data = dict()
            d_data['xh'] = xh
            d_data['xnxq'] = settings.XNXQID
            d_data['teacher'] = data['group']['teacher']
            d_data['validTimesNormal'] = data['info']['validTimes']
            d_data['achievements'] = data['achievements']
            if data['success']:
                return Response(status=status.HTTP_200_OK, data=d_data)
            else:
                return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)
