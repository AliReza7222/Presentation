from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from Slide.api.v1.serializers import SlideSerializer


class CreateSlideView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SlideSerializer
