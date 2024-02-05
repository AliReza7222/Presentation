from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from Slide.serializers import SlideSerializer
from Slide.models import Slide


class SlideViewSet(
    GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    
    permissions_classes = (IsAuthenticated, )
    serializer_class = SlideSerializer
    queryset = Slide.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            data={'message': 'The slide was successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
