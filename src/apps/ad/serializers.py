from rest_framework import serializers
from .models import DefaultAD
import datetime


class ADSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAD
        fields = ('id', 'ad_img', 'ad_text', 'tag_a_text', 'tag_a_color', 'tag_b_text', 'tag_b_color', 'button_text',
                  'button_color', 'type', 'additional_field_a', 'additional_field_b')
