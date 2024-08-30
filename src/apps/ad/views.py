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

from .models import ADLog, DefaultAD
from .serializers import ADSerializer


from django.conf import settings
import redis
import random
import datetime


# Create your views here.

class GetAd(APIView):
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DefaultAD.objects.filter(valid_time__gte=datetime.datetime.now())

    def get_ad(self, open_id):
        query_set = self.get_queryset()
        l_ad = []
        for ad in query_set:
            rate = ad.rate
            seconds = rate.split('/')[0]
            times = rate.split('/')[1]
            count = ADLog.objects.filter(createTime__range=[datetime.datetime.now() - datetime.timedelta(seconds=int(seconds)), datetime.datetime.now()],
                                         openId=open_id, ad_id=ad.id).count()
            if count < int(times):
                l_ad.append(ad)

        if len(l_ad) == 0:
            return None
        else:
            return random.choice(l_ad)

    def get(self, request):
        user = request.user
        try:
            ad = self.get_ad(user.openId)
            if ad:
                serializer = ADSerializer(ad)

                ad_log = ADLog(ad_id=ad.id, openId=user.openId)
                ad_log.save()

                return Response(serializer.data)
            else:
                return Response({})
        except Exception as e:
            return Response(exception=True, status=status.HTTP_400_BAD_REQUEST)
