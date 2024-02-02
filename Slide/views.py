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

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return Response(serializer.data)


class DeleteSlideView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Slide.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'message': 'The slide was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
