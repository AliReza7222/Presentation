import uuid, re
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

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
            'password': {'write_only': True},
        }

    def validate_username(self, username):
        if len(username) <= 6 or len(username) >= 21:
            raise serializers.ValidationError("The number of characters in the username must be greater than 7 and less than 20 characters !")
        elif not re.match('^[a-zA-Z].+$', username):
            raise serializers.ValidationError("The username start with words !")
        return username

    def validate_password(self, password):
        if len(password) <= 6:
            raise serializers.ValidationError('The minimum number of password characters must be greater than 7 !')
        return password

    def validate_activation_code(self, activation_code):
        if not len(activation_code) == 16:
            raise serializers.ValidationError('Invalid activation code !')
        return activation_code

    def validate(self, data):
        password, confirm_password = data["password"], data["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "password do not match with confirm password !"}
            )
        return data

    def create(self, validated_data):
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class ProfileSrializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'updated_at'
        ]


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email, password = data.get("email"), data.get("password")

        check_email_user = User.objects.filter(email=email)
        error_message = {"email or password": "Invalid email or password"}
        if not check_email_user.exists():
            raise serializers.ValidationError(error_message)

        user = check_email_user.get()

        if not check_password(password, user.password):
            raise serializers.ValidationError(error_message)

        refresh_token = RefreshToken.for_user(user=user)

        data = {
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
            'user_id': str(user.id)
        }
        return data
