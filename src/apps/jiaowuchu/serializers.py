from rest_framework import serializers
from .models import JiaoWuChuNews


class CreateJiaoWuChuNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiaoWuChuNews
        fields = '__all__'


class ListJiaoWuChuNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiaoWuChuNews
        fields = '__all__'
