from rest_framework import serializers
from .models import LikeToComment, FavToContent, LikeToContent


class CreateLikeToContentSerializer(serializers.Serializer):
    contentId = serializers.IntegerField()

    def validate_contentId(self, contentId):
        return contentId



class CreateFavToContentSerializer(serializers.Serializer):
    contentId = serializers.IntegerField()

    def validate_contentId(self, contentId):
        return contentId


class CreateLikeToCommentSerializer(serializers.Serializer):
    commentId = serializers.IntegerField()

    def validate_contentId(self, commentId):
        return commentId


class FavListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = FavToContent


class CreateReportToContentSerializer(serializers.Serializer):
    contentId = serializers.IntegerField()

    def validate_contentId(self, contentId):
        return contentId
