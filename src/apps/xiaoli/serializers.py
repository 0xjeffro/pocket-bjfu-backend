from rest_framework import serializers
from .models import XiaoLi


class ListXiaoLiSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiaoLi
        fields = '__all__'
