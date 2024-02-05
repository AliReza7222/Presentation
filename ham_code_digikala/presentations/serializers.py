from django.db import transaction
from rest_framework import serializers

from .models import *


class PresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = '__all__'