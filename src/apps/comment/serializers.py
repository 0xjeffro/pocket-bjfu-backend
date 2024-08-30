from rest_framework import serializers
from .models import Comment

from apps.content.models import Content
from apps.operate.models import LikeToComment
import datetime


class CreateCommentSerializer(serializers.Serializer):
    commentText = serializers.CharField(max_length=300)
    deep = serializers.IntegerField()
    reply = serializers.IntegerField()
    contentId = serializers.IntegerField()
    commentId = serializers.IntegerField()

    def validate_commentText(self, commentText):
        return commentText

    def validate_deep(self, deep):
        return deep

    def validate_reply(self, reply):
        return reply

    def validate_contentId(self, contentId):
        return contentId

    def validate_commentId(self, commentId):
        return commentId


class ListCommentSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(label='发布时间')
    isLike = serializers.SerializerMethodField(label='是否点赞')
    isAuthor = serializers.SerializerMethodField(label='是否是楼主')

    class Meta:
        model = Comment
        fields = ('id', 'openId', 'commentText', 'time', 'isLike', 'isAuthor', 'nLike', 'deep', 'reply', 'contentId',
                  'commentId', 'state')

    def get_time(self, obj):
        createTime = obj.createTime
        now = datetime.datetime.now()
        timedelta = now - createTime
        seconds = timedelta.total_seconds()
        if seconds <= 60 * 15:
            if seconds <= 60:
                return '刚刚'
            else:
                return str(int(seconds/60)) + '分钟前'

        return createTime.strftime('%Y/%m/%d %H:%M')

    def get_isLike(self, obj):
        # user = self.context['request'].user
        # openId = user.openId
        # commentId = obj.id
        # records = LikeToComment.objects.filter(openId=openId, commentId=commentId)
        # if records.count() == 0:
        #     return False
        # else:
        #     return True
        return obj.is_like

    def get_isAuthor(self, obj):
        # commentAuthor = obj.openId
        # contentId = obj.contentId
        # content = Content.objects.get(id=contentId)
        # contentAuthor = content.openId
        # return commentAuthor == contentAuthor
        return obj.content_author == obj.openId
