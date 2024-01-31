from rest_framework import serializers

from presentations.models import *


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
