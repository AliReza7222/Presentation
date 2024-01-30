from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from accounts.api.v1.serializers import *
from accounts.models import Profile


class SignUpUserView(CreateAPIView):
    serializer_class = UserSerializer


class SignInUserView(TokenObtainPairView):
    serializer_class = SignInSerializer


class UpdateProfileUserView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSrializer
    queryset = Profile.objects.all()
