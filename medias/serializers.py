from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )
