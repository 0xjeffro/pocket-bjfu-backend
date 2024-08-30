from django.shortcuts import render
from rest_framework import mixins, generics, viewsets
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from rest_framework.views import APIView

from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from rest_framework.response import Response
from rest_framework import status

from .models import ChangYongLianJie
from .serializers import ListChangYongLianJieSerializer


# Create your views here.


class ChangYongLianJieViewSet(CacheResponseMixin, viewsets.GenericViewSet,
                              mixins.ListModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['priority', ]

    def get_queryset(self):
        return ChangYongLianJie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListChangYongLianJieSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]


class ChangYongLianJieAddPriority(APIView):
    """
    POST:
        接受 id: 链接的id
        将此链接的 priority + 1
    """
    throttle_classes = (UserRateThrottle, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request):
        data = request.data
        try:
            link_id = data['id']
            link = ChangYongLianJie.objects.get(id=link_id)
            link.priority += 1
            link.save()

            return Response(status=status.HTTP_200_OK, data={})
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)