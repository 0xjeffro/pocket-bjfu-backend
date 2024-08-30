from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment
from apps.operate.models import LikeToComment
from apps.content.models import Content
from .serializers import CreateCommentSerializer, ListCommentSerializer
from .filters import CommentListFilter

from utils.sendSubscribeMessage import send_reply_subscribe_message

from django.db import transaction
from django.db.models import Exists, OuterRef, F, Subquery

from utils.msgSecSheck import msg_sec_check, key_words_check

from django.conf import settings
import redis

from apps.content.views import update_priority

# Create your views here.

class CommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = CommentListFilter
    ordering_fields = ['priority', 'createTime', 'id']
    search_fields = ['contentId']

    def get_queryset(self):
        if self.action == 'list':
            import time
            time.sleep(0.4)
            contentId = self.request.GET.get('contentId', None)
            if contentId is not None:
                openId = self.request.user.openId
                content = Content.objects.filter(id=contentId)
                return Comment.objects.annotate(content_author=Subquery(content.values('openId')[:1])).annotate(
                    is_like=Exists(LikeToComment.objects.filter(openId=openId, commentId=OuterRef('id')))
                ).all()
            else:
                return Comment.objects.all()
        return Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCommentSerializer
        if self.action == 'list':
            return ListCommentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB,
                                  password=settings.REDIS_PWD)

            openId = request.user.openId
            commentText = serializer.validated_data['commentText']
            deep = serializer.validated_data['deep']
            reply = serializer.validated_data['reply']
            contentId = serializer.validated_data['contentId']
            commentId = serializer.validated_data['commentId']

            state = msg_sec_check(commentText)
            if state != 0:
                _, state, _ = key_words_check(commentText, openId, '评论')

            fast_click_cache = r.get('{0}_fastClick_comment'.format(openId))

            if fast_click_cache is None:
                with transaction.atomic():
                    comment = Comment(openId=openId, commentText=commentText, deep=deep, reply=reply, contentId=contentId,
                                      commentId=commentId, state=state)
                    comment.save()

                    update_priority(contentId, scene='createComment')  # 更新优先级

                    content = Content.objects.get(id=contentId)
                    content.nComment += 1
                    content.save()

                r.set('{0}_fastClick_comment'.format(openId), commentText, ex=5)

                if reply == -1:  # 一级评论的reply字段为-1
                    content = Content.objects.get(id=contentId)
                    page = 'pages/index/detail/detail?id={0}'.format(contentId)
                    if openId != content.openId:
                        send_reply_subscribe_message(toUser=content.openId, page=page, text=commentText)
                else:
                    #  reply不为-1，说明是评论的评论（二级评论）
                    comment = Comment.objects.get(id=reply)
                    page = 'pages/commentDetail/commentDetail?contentId={0}&commentId={1}'.format(contentId, commentId)
                    if openId != comment.openId:
                        send_reply_subscribe_message(toUser=comment.openId, page=page, text=commentText)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)