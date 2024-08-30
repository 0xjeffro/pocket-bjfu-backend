from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, filters

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from .models import Content
from apps.users.models import UserProfile
from apps.rules.models import ColdUser, ColdContent
from apps.operate.models import LikeToContent, FavToContent
from apps.comment.models import Comment
from .serializers import CreateContentSerializer, ListContentSerializer, UpdateContentSerializer
from .pagination import ContentPagination

from .permission import IsContentAuthorOrAdmin

from utils.msgSecSheck import msg_sec_check, key_words_check

from django.conf import settings
import redis
import time
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnList

# Create your views here.


def update_priority(content_id, scene='createContent'):
    import math
    content = Content.objects.get(id=content_id)

    if scene == 'createContent':
        content.priority = time.time() + content.priority_delta
        content.save()

        return

    if scene == 'like':
        content.priority = content.priority + 30 + content.priority_delta
        content.save()
        return

    if scene == '-like':
        content.priority = content.priority - 30 + content.priority_delta
        content.save()
        return

    if scene == 'createComment':
        content.priority = time.time() + math.log(max(content.nLike, 1), 2) * 60 + content.priority_delta
        content.save()
        return


def get_content_relate_users(contentId):

    """
    获取已经与该contentId产生交互的openId列表
    """
    users = []
    contents = Content.objects.filter(id=contentId)
    for _ in contents:  # 发帖人
        users.append(_.openId)

    comments = Comment.objects.filter(contentId=contentId)
    for _ in comments:  # 评论者
        users.append(_.openId)

    favs = FavToContent.objects.filter(contentId=contentId)
    for _ in favs:  # 收藏者
        users.append(_.openId)

    likes = LikeToContent.objects.filter(contentId=contentId)
    for _ in likes:  # 点赞者
        users.append(_.openId)

    return users


class ContentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = ContentPagination
    ordering_fields = ['priority', 'createTime', 'id']
    search_fields = ['id', 'contentText']

    def get_queryset(self):
        return Content.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateContentSerializer
        if self.action == 'list':
            return ListContentSerializer
        if self.action == 'retrieve':
            return ListContentSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateContentSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            return [IsAuthenticated(), IsContentAuthorOrAdmin()]
        return [IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        # return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.DB,
                              password=settings.REDIS_PWD)

        openId = request.user.openId
        contentText = serializer.validated_data['contentText']
        contentImg = serializer.validated_data['contentImg']

        state = msg_sec_check(contentText)

        priority_keywords_delta = 0
        if state != 0:
            state, _, priority_keywords_delta = key_words_check(contentText, openId, '帖子')

        fast_click_cache = r.get('{0}_fastClick_content'.format(openId))

        if fast_click_cache is None:
            # 生成装饰icon逻辑开始
            import datetime
            icon = ''
            if datetime.datetime(2021, 6, 1, 0, 0) < datetime.datetime.now() < datetime.datetime(2021, 9, 15, 0, 0) \
                    and UserProfile.objects.get(openId=openId).verifyType == '2':
                    icon = 'https://pocket-bfu-img.bfuer.com/xl-tree.png'
            # 生成icon逻辑结束

            # 获取初始化权重
            priority_delta = 0
            try:
                xh = UserProfile.objects.get(openId=openId)
                priority_delta = ColdUser.objects.get(xh=xh).delta
            except:
                priority_delta = 0

            content = Content(openId=openId, contentText=contentText, contentImg=contentImg, state=state
                              , decoration_url=icon, priority_delta=priority_delta + priority_keywords_delta)
            content.save()

            update_priority(content.id)
            r.set('{0}_fastClick_content'.format(openId), contentText, ex=8)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            if request.GET.get('search') is None:
                openId = request.user.openId
                page_number = request.GET.get('page')
                cold_content = {_.contentId: _.page_number for _ in ColdContent.objects.all()}

                serializer = self.get_serializer(page, many=True)
                for content in serializer.data:
                    if content['id'] in cold_content.keys():  # 如果该内容id在冷却列表中
                        relate_users = get_content_relate_users(content['id'])
                        if openId not in relate_users:  # 且当前用户与该帖未产生相关关系
                            content['state'] = 'co'  # 冷却

                for key, val in cold_content.items():
                    if val == int(page_number):

                        content = Content.objects.get(id=key)
                        c_serializer = self.get_serializer(content)

                        return self.get_paginated_response(list(serializer.data) + [OrderedDict(c_serializer.data)])
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MyContentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = ContentPagination
    ordering_fields = ['priority', 'createTime', 'id']

    def get_queryset(self):
        user = self.request.user
        openId = user.openId
        return Content.objects.filter(openId=openId)

    def get_serializer_class(self):
        if self.action == 'list':
            return ListContentSerializer

    def get_permissions(self):
        return [IsAuthenticated(), ]