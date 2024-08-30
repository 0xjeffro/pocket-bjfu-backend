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

from .models import CaptureScreenTracking
from .serializers import CaptureScreenTrackingSerializer


from django.conf import settings
import redis
import random
import datetime

# Create your views here.


class CaptureScreenTrackingViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
            return CaptureScreenTracking.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CaptureScreenTrackingSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        openId = request.user.openId
        pageUrl = serializer.validated_data['pageUrl']
        options = serializer.validated_data['options']

        c = CaptureScreenTracking(openId=openId, pageUrl=pageUrl, options=options)
        c.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)