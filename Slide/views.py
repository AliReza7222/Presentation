from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from Slide.serializers import SlideSerializer
from Slide.models import Slide


class CreateSlideView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SlideSerializer


class UpdateSlideView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SlideSerializer
    queryset = Slide.objects.all()

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


class DeleteSlideView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Slide.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'message': 'The slide was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
