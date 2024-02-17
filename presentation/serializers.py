from django.db import transaction
from slugify import slugify
from rest_framework import serializers

from .models import Presentation


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields ="__all__"
        extra_kwargs = {
            'user': {'read_only': True},
            'slug': {'read_only': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
