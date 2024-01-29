from rest_framework.generics import CreateAPIView

from accounts.api.v1.serializers import *


class SignUpUserView(CreateAPIView):
    serializer_class = UserSerializer
