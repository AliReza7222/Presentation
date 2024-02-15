from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from .models import Presentation


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields ="__all__"
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate_slug(self, slug):
        slug = slugify(slug)
        if not slug:
            raise serializers.ValidationError("Please enter a valid slug !")
        return slug

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
