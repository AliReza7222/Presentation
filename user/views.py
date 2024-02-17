from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import (CreateAPIView, UpdateAPIView, GenericAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import Profile, User
from presentation.models import Presentation
from slide.models import Slide
from .models import Profile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RegisterUserView(CreateAPIView):
    """
        The activation_code field must be sent to the email that the email
        sending section is not implemented due to the lack of a server, so when creating a user,
        we show this activation_code field to the user so that he can activate the account.
        In fact, we are in the test!
    """
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]


class LoginUserView(TokenObtainPairView):
    serializer_class = LoginSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]


class UpdateProfileUserView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSrializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

    def patch(self, request, *args, **kwargs):
        instance = request.user.profile

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveUserView(GenericAPIView):
    serializer_class = ActiveUserSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(activation_code=request.data.get('activation_code'))
        if not user.exists():
            return Response({'message': 'InValid activation_code'}, status=status.HTTP_400_BAD_REQUEST)

        user = user.get()
        user.is_active = True
        user.save()
        return Response(
            {'message': 'Your account has been successfully activated.'},
            status= status.HTTP_200_OK
        )


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"message": "successfully password changed "}, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message" : "rest your password . (test)"}, status=status.HTTP_200_OK)


class DashboardView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        presentations = Presentation.objects.filter(user=request.user)
        total_views_count = presentations.aggregate(total_views_count=Sum('cnt_view'))
        presentations_count = presentations.count()
        slides_count = 0
        for presentation in presentations:
            slide_count = Slide.objects.filter(presentation_id= presentation).count()
            slides_count += slide_count
        data = {
                "presentation_cont" : presentations_count,
                "slide_count" : slides_count,
                "presentation_views" : total_views_count.get('total_views_count', 0),
                }
        return Response(data, status=status.HTTP_200_OK)
