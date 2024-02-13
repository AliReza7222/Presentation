from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import Profile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RegisterUserView(CreateAPIView):
    serializer_class = UserSerializer


class LoginUserView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UpdateProfileUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSrializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user.profile

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

# manual_parameters
old_password = openapi.Parameter('Old password', in_=openapi.TYPE_INTEGER,
                           type=openapi.TYPE_INTEGER)
new_password =  openapi.Parameter('New password', in_=openapi.TYPE_INTEGER,
                           type=openapi.TYPE_INTEGER)
renew_password =  openapi.Parameter('Repeat password', in_=openapi.TYPE_INTEGER,
                           type=openapi.TYPE_INTEGER)
email = openapi.Parameter('Email', in_=openapi.TYPE_STRING,
                           type=openapi.FORMAT_EMAIL)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters= [old_password,new_password,renew_password])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={"user": request.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "password changed"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters= [email],)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "this message for test"}, status=status.HTTP_200_OK)
