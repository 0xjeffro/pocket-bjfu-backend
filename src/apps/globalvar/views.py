from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, filters

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .models import GlobalVar
from .serializers import GlobalVarSerializer

from django.conf import settings
import redis
import time

# Create your views here.


class GlobalVarViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
        return GlobalVar.objects.all()

    def get_serializer_class(self):
        return GlobalVarSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.key == 'AD_TYPE_FUCK':

            r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB,
                                  password=settings.REDIS_PWD)
            cache = r.get('ad_count_{0}_cache'.format(request.user.openId))
            if cache is not None:
                r.set('ad_count_{0}_cache'.format(request.user.openId), str(int(cache) + 1))
                if int(cache) > 100:
                    instance.value = str(-1)
            else:
                r.set('ad_count_{0}_cache'.format(request.user.openId), str(1), ex=86400)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)