from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .models import Notice
from .serializers import NoticeSerializer


from django.conf import settings
import redis
import random
import datetime


class GetNotice(APIView):
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notice.objects.all().order_by('-priority')

    def get(self, request):
        try:
            component = request.GET.get('component')
            user = request.user
            xh = user.xh

            notice = None
            notices = self.get_queryset()

            for n in notices:
                if n.xh_startswith == xh[:len(n.xh_startswith)] and n.show and n.component == component:
                    notice = n
                    break

            if notice:
                serializer = NoticeSerializer(notice)
                return Response(serializer.data)
            else:
                return Response({})

        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)