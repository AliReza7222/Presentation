from django.db import transaction
from rest_framework import serializers

from .models import Presentation


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields ="__all__"
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)
