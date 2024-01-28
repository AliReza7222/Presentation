from rest_framework import serializers

from Slide.models import Slide


class SlideSerializer(serializers.Modelserializer):
    class Meta:
        model = Slide
        fields = '__all__'
