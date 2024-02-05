from tabnanny import verbose
import uuid
from django.core.validators import EmailValidator
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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    renew_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"password": "Your previous password is wrong"})
        return value
    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("renew_password"):
            raise serializers.ValidationError(
                {"password" : "new passwords are not same"})
        return attrs
    def create(self, validated_data):
        user = self.context["user"]
        user.set_password(validated_data["new_password"])
        user.save()
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"email": str(e)})
        return value

    def validate(self, data):
        email = data.get("email")
        
        check_email_user = User.objects.filter(email=email)
        if not check_email_user.exists():
            raise serializers.ValidationError(
                {"email": "Invalid email"})
        return data
