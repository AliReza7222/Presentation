from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from utils.create_code import CreateCode

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'created_at',
            'is_active',
            'activation_code',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'activation_code': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def validate_username(self, username):
        if len(username) <= 6 or len(username) >= 21:
            raise serializers.ValidationError(
                {"username": "The number of characters in the username must be greater than 7 and less than 20 characters !"}
            )
        return username

    def validate_password(self, password):
        if len(password) <= 6:
            raise serializers.ValidationError(
                {"password": "The minimum number of password characters must be greater than 7 !"}
            )
        return password

    def validate(self, data):
        password, confirm_password = data.get("password"), data.get("confirm_password")
        if password and password != confirm_password:
            raise serializers.ValidationError(
                {"password": "password do not match with confirm password !"}
            )
        return data

    def create(self, validated_data):
        del validated_data["confirm_password"]
        validated_data["password"] = make_password(validated_data["password"])
        validated_data['activation_code'] = CreateCode.get_token()
        return super().create(validated_data)


class ProfileSrializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email, password = data.get("email"), data.get("password")
        user = self._validate_user(email, password)
        response = self._generate_tokens(user)
        return response

    def _validate_user(self, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error_message": "Invalid email or password"})

        if not user.check_password(password):
            raise serializers.ValidationError({"error_message": "Invalid email or password"})

        return user

    def _generate_tokens(self, user):
        refresh_token = RefreshToken.for_user(user=user)
        return {
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
            'user': self._serialize_user(user)
        }

    def _serialize_user(self, user):
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "profile": self._serialize_profile(user.profile)
        }

    def _serialize_profile(self, profile):
        request = self.context['request']
        return {
            "id": str(profile.id),
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "avatar": request.build_absolute_uri(profile.avatar.url) if profile.avatar else None,
            "bio": profile.bio
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    renew_password = serializers.CharField(write_only=True)

    def validate_old_password(self, old_password):
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Your old password is wrong !")
        return old_password

    def validate_new_password(self, new_password):
        if len(new_password) <= 6:
            raise serializers.ValidationError(
                "The minimum number of new password characters must be greater than 7 !"
            )
        return new_password

    def validate(self, data):
        if data.get("new_password") != data.get("renew_password"):
            raise serializers.ValidationError(
                {"password": "new passwords are not same"})
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data["new_password"])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        if not User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError(
                {"email": "Invalid email"})
        return data


class ActiveUserSerializer(serializers.Serializer):
    activation_code = serializers.CharField(write_only=True)
