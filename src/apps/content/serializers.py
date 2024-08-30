from rest_framework import serializers
from .models import Content
from apps.users.models import UserProfile
from apps.globalvar.models import GlobalVar
from apps.operate.models import LikeToContent, FavToContent, ReportToContent
import datetime


class CreateContentSerializer(serializers.Serializer):
    contentText = serializers.CharField(max_length=1500)
    contentImg = serializers.CharField(max_length=2000, allow_blank=True)

    def validate_contentText(self, contentText):
        return contentText

    def validate_contentImg(self, contentImg):
        return contentImg


class ListContentSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField(label='发布时间')
    isLike = serializers.SerializerMethodField(label='是否点赞')
    isFav = serializers.SerializerMethodField(label='是否收藏')
    state = serializers.SerializerMethodField(label='帖子状态过滤')

    class Meta:
        model = Content
        fields = ('id', 'openId', 'contentText', 'contentImg', 'time', 'isLike', 'isFav', 'nLike', 'nComment',
                  'decoration_url', 'state')

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
        user = self.context['request'].user
        openId = user.openId
        contentId = obj.id
        records = LikeToContent.objects.filter(openId=openId, contentId=contentId)
        if records.count() == 0:
            return False
        else:
            return True

    def get_isFav(self, obj):
        user = self.context['request'].user
        openId = user.openId
        contentId = obj.id
        records = FavToContent.objects.filter(openId=openId, contentId=contentId)
        if records.count() == 0:
            return False
        else:
            return True

    def get_state(self, obj):
        user = self.context['request'].user
        author = UserProfile.objects.get(openId=obj.openId)
        if obj.state == '4':  # 仅同班可见, 如171002412
            if len(user.xh) == 9:  # 本科生学号9位
                if user.xh[:7] != author.xh[:7]:
                    return 'class-cold'
                else:
                    return '1'
        if obj.state == '5':  # 仅同级同专业可见
            if len(user.xh) == 9:  # 本科生学号9位
                if user.xh[:6] != author.xh[:6]:
                    return 'major-cold'
                else:
                    return '1'
        if obj.state == '6':  # 仅同级同学院可见
            if len(user.xh) == 9:  # 本科生学号9位
                if user.xh[:5] != author.xh[:5]:
                    return 'academy-cold'
                else:
                    return '1'

        if obj.state == '7':  # 仅自己可见
            if len(user.xh) == 9:  # 本科生学号9位
                if user.xh != author.xh:
                    return 'self-cold'
                else:
                    return '1'

        # 如果当前请求用户不喜欢该内容则不展示
        records = ReportToContent.objects.filter(openId=user.openId, contentId=obj.id)
        if records.count() != 0:
            return 'dislike'

        return obj.state


class UpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('state', )