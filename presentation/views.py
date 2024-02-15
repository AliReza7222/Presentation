from django.db import transaction
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Presentation, Tag
from utils.tags import TagOperations
from .serializers import *


class CreatePresentationView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    parser_classes = [MultiPartParser]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # get data with list tag object
        data = TagOperations.get_and_set_tags(request.data.copy())
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UpdatePresentationView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    parser_classes = [MultiPartParser]
    queryset = Presentation.objects.all()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_copy = request.data.copy()

        # get data with list tag object
        data = TagOperations.get_and_set_tags(data_copy)

        serializer = self.get_serializer(
            instance,
            data=data,
            partial=kwargs.get('partial', False)
        )
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        # delete tags ==> null presentation
        null_tags = list(
            Tag.objects.filter(presentation__isnull=True).values_list('id', flat=True)
        )
        if null_tags:
            TagOperations.delete_tag(null_tags)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class DeletePresentationView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Presentation.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        list_tags_id = list(instance.tags.values_list('id', flat=True))
        TagOperations.delete_tag(list_tags_id)
        self.perform_destroy(instance)
        return Response(
            {'message': 'The presentation was successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
