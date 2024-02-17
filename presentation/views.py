from django.db import transaction
from django.core.paginator import Paginator
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView
)
from django.shortcuts import get_object_or_404
from .serializers import PresentationSerializer
from .models import Presentation, Tag
from slide.models import Slide
from utils.tags import TagOperations
from .serializers import *


class CreatePresentationView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

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
    parser_classes = [MultiPartParser, JSONParser, FormParser]
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


class ListPresentationView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PresentationSerializer

    def get_queryset(self):
        queryset = Presentation.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        page_obj = Paginator(queryset, 5)
        response = {
            "pagination":{
                "count": page_obj.count,
                "data_per_page": 5,
                "page_number": page_obj.num_pages
            },
            "data": serializer.data
        }
        return Response(
            response,
            status = status.HTTP_200_OK
        )


class PresentationSlideListView(ListAPIView):
    def get(self, request, presentation_id):
        presentation = get_object_or_404(Presentation, id=presentation_id)
        slides = Slide.objects.filter(presentation_id=presentation.id)
        data =[{
                'section_link': slide.section_link,
                'section_id': slide.section_id,
                'content': slide.content,
            }
            for slide in slides]
        return Response({"slides" : data}, status=status.HTTP_200_OK)


class PresentationSlidesView(ListAPIView):
    def get(self, request, slug):
        try:
            presentation = get_object_or_404(Presentation, slug=slug)
            slides = Slide.objects.filter(presentation_id=presentation.id)
            presentation.increment_views_count()
            data =[{
                    'section_link': slide.section_link,
                    'section_id': slide.section_id,
                    'content': slide.content,
                }
                for slide in slides]

            return Response({'slides': data}, status=status.HTTP_200_OK)

        except Presentation.DoesNotExist:
            return Response({"error": "Presentation not found"}, status=status.HTTP_404_NOT_FOUND)
