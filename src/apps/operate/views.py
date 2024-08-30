from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from apps.content.models import Content
from apps.comment.models import Comment
from .models import LikeToContent, LikeToComment, FavToContent, ReportToContent
from .serializers import CreateLikeToContentSerializer, CreateFavToContentSerializer, CreateLikeToCommentSerializer, \
    FavListSerializer, CreateReportToContentSerializer
from .pagination import FavListPagination

from django.db import transaction
from apps.content.views import update_priority


class LikeToContentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
            return LikeToContent.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLikeToContentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            openId = request.user.openId
            contentId = serializer.validated_data['contentId']
            records = LikeToContent.objects.filter(openId=openId, contentId=contentId)

            if records.count() == 0:
                with transaction.atomic():
                    record = LikeToContent(openId=openId, contentId=contentId)
                    record.save()

                    content = Content.objects.get(id=contentId)
                    content.nLike += 1
                    content.save()
                    update_priority(contentId, scene='like')

            else:
                with transaction.atomic():
                    record = records[0]
                    record.delete()

                    content = Content.objects.get(id=contentId)
                    content.nLike -= 1
                    content.save()
                    update_priority(contentId, scene='-like')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FavToContentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
            return FavToContent.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFavToContentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            openId = request.user.openId
            contentId = serializer.validated_data['contentId']

            records = FavToContent.objects.filter(openId=openId, contentId=contentId)

            if records.count() == 0:
                record = FavToContent(openId=openId, contentId=contentId)
                record.save()
            else:
                record = records[0]
                record.delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LikeToCommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
            return LikeToComment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLikeToCommentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            openId = request.user.openId
            commentId = serializer.validated_data['commentId']
            records = LikeToComment.objects.filter(openId=openId, commentId=commentId)

            if records.count() == 0:
                with transaction.atomic():
                    record = LikeToComment(openId=openId, commentId=commentId)
                    record.save()

                    comment = Comment.objects.get(id=commentId)
                    comment.nLike += 1
                    comment.save()

            else:
                with transaction.atomic():
                    record = records[0]
                    record.delete()

                    comment = Comment.objects.get(id=commentId)
                    comment.nLike -= 1
                    comment.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyFavViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = FavListPagination
    ordering_fields = ['createTime', 'id']

    def get_queryset(self):
        user = self.request.user
        openId = user.openId
        return FavToContent.objects.filter(openId=openId)

    def get_serializer_class(self):
        if self.action == 'list':
            return FavListSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]


class ReportToContentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
            return ReportToContent.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReportToContentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            openId = request.user.openId
            contentId = serializer.validated_data['contentId']

            record = ReportToContent(openId=openId, contentId=contentId)
            record.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


