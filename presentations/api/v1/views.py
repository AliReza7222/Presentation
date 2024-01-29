from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from presentations.api.v1.serializers import PresentationSerializer, TagSerializer


class CreatePresentationView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PresentationSerializer


class CreateTagView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
