from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import PresentationSerializer
from .models import Presentation, Tag
from utils.tags import TagObject


class CreatePresentationView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    tag_class = TagObject()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        data_copy['user'] = request.user.id

        # get data and get tags list ==> (data, tags)
        data, tags = self.tag_class.get_and_set_tags(data_copy)

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.tag_class.add_tags_valid_data(serializer, tags),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UpdatePresentationView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    queryset = Presentation.objects.all()
    tag_class = TagObject()


    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_copy = request.data.copy()
        data_copy['user'] = request.user.id

        # get data and get tags list ==> (data, tags)
        data, tags = self.tag_class.get_and_set_tags(data_copy)

        serializer = self.get_serializer(
            instance,
            data=data,
            partial=kwargs.get('partial', False)
        )
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        # delete tag ==> null presentation
        null_tags = list(
            Tag.objects.filter(presentation__isnull=True).values_list('id', flat=True)
        )
        if null_tags:
            self.tag_class.delete_tag(null_tags)

        return Response(
            self.tag_class.add_tags_valid_data(serializer, tags),
            status=status.HTTP_200_OK
        )


class DeletePresentationView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Presentation.objects.all()
    tag_class = TagObject()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        list_tags_id = list(instance.tags.values_list('id', flat=True))
        self.tag_class.delete_tag(list_tags_id)
        self.perform_destroy(instance)
        return Response(
            data={'message': 'The presentation was successfully deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
