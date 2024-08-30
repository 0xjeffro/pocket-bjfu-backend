from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_extensions.mixins import CacheResponseMixin

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import JiaoWuChuNews
from .serializers import CreateJiaoWuChuNewsSerializer, ListJiaoWuChuNewsSerializer
from .filters import JiaoWuChuNewsFilter
from .pagination import NewsPagination
# Create your views here.


class JiaoWuChuNewsViewSet(CacheResponseMixin, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_class = JiaoWuChuNewsFilter
    ordering_fields = ['time', ]
    pagination_class = NewsPagination

    def get_queryset(self):
        return JiaoWuChuNews.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateJiaoWuChuNewsSerializer
        elif self.action == 'list':
            return ListJiaoWuChuNewsSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]
