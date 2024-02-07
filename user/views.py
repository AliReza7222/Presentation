from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import Profile


class SignUpUserView(CreateAPIView):
    serializer_class = UserSerializer


class SignInUserView(TokenObtainPairView):
    serializer_class = SignInSerializer


class UpdateProfileUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSrializer
    queryset=Profile.objects.all()


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user.profile

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={"user": request.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response("password changed", status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "this message for test"}, status=status.HTTP_200_OK)
