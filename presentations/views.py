from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from presentations.serializers import *
from presentations.models import Presentation, Tag
from utils.tag_create import CreateObjectTag


class CreatePresentationView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PresentationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        tags = data.pop('tags', [])

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        if tags:
            data.setlist('tags', CreateObjectTag.create_list_obj_tags(tag_names=tags))

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            CreateObjectTag.add_tags_valid_data(serializer, tags),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UpdatePresentationView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PresentationSerializer
    queryset = Presentation.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response(serializer.data)


class DeletePresentationView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Presentation.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'message': 'The presentation was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
