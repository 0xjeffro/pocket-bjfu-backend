from rest_framework import serializers
from .models import CaptureScreenTracking


class CaptureScreenTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptureScreenTracking
        fields = ('pageUrl', 'options')