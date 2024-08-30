from rest_framework import serializers
from .models import GlobalVar


class GlobalVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVar
        fields = '__all__'
