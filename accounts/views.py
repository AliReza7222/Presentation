from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.serializers import *
from accounts.models import Profile


class SignUpUserView(CreateAPIView):
    serializer_class = UserSerializer


class SignInUserView(TokenObtainPairView):
    serializer_class = SignInSerializer


class UpdateProfileUserView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSrializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
