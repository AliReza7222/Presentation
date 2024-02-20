from django.db import transaction
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from .models import Presentation, Tag
from .serializers import PresentationSerializer
from slide.serializers import SlideSerializer
from utils.tags import TagOperations
from utils.data_presentation import GetDataPresentation
from .serializers import *


class CreatePresentationView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # get data with list tag object
        data, tags = TagOperations.get_tags(request.data.copy())
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        instance.tags.set(tags)
        headers = self.get_success_headers(serializer.data)
        return Response(
            TagOperations.data_with_tags_name(serializer.data),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UpdatePresentationView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    queryset = Presentation.objects.all()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # get data with list tag object
        data, tags = TagOperations.get_tags(request.data.copy())

        serializer = self.get_serializer(
            instance,
            data=data,
            partial=kwargs.get('partial', False)
        )
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        instance.tags.set(tags)

        # delete tags ==> null presentation
        null_tags = list(
            Tag.objects.filter(presentation__isnull=True).values_list('id', flat=True)
        )
        if null_tags:
            TagOperations.delete_tag(null_tags)

        return Response(
            TagOperations.data_with_tags_name(serializer.data),
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


class ListPresentationView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PresentationSerializer

    def get_queryset(self):
        queryset = Presentation.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        page_obj = Paginator(queryset, 5)
        print(serializer.data, 'awkdoakwdkaowdk00000')
        response = {
            "pagination":{
                "count": page_obj.count,
                "data_per_page": 5,
                "page_number": page_obj.num_pages
            },
            "data": [
                TagOperations.data_with_tags_name(presentation) for presentation in serializer.data
            ]
        }
        return Response(
            response,
            status = status.HTTP_200_OK
        )


class PresentationView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PresentationSerializer
    queryset = Presentation.objects.all()

    def retrieve(self, request, *args, **kwargs):
        presentation = self.get_object()
        data = GetDataPresentation.data_presentation(presentation, self.get_serializer(presentation))
        return Response({"data" : data}, status=status.HTTP_200_OK)


class PresentationBySlugView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PresentationSerializer
    queryset = Presentation.objects.all()
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        presentation = self.get_object()
        data = GetDataPresentation.data_presentation(presentation,
            self.get_serializer(presentation), slug_request=True)
        return Response({"data": data}, status=status.HTTP_200_OK)
