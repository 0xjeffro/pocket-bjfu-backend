from django.shortcuts import render
from rest_framework import mixins, generics, viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import XiaoLi
from .serializers import ListXiaoLiSerializer

# Create your views here.


class XiaoLiViewSet(CacheResponseMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # serializer_class = CreateWallSerializer
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['priority', ]

    def get_queryset(self):
        return XiaoLi.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListXiaoLiSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]
