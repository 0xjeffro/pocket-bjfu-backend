from rest_framework import serializers
from .models import ChangYongLianJie


class ListChangYongLianJieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangYongLianJie
        fields = '__all__'
