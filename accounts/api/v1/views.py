from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.serializers import *


class SignUpUserView(CreateAPIView):
    serializer_class = UserSerializer


class SignInUserView(TokenObtainPairView):
    serializer_class = SignInSerializer
