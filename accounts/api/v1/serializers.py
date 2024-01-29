import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'created_at',
            'activation_code'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'activation_code': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate(self, data):
        password, confirm_password = data["password"], data["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)



class ProfileSrializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
