from rest_framework import serializers


class GetUrlSrializer(serializers.Serializer):
    url = serializers.CharField()
