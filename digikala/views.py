from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import GetUrlSrializer
from utils.data_digikala import DigiKalaData


class GetChaptersView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        data = DigiKalaData.get_chapters()
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status=status_request)


class GetSectionView(APIView):
    permission_classes = (IsAuthenticated, )
    slug = openapi.Parameter('slug', openapi.IN_QUERY,
                             type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[slug])
    def get(self, request, **kwargs):
        slug = request.query_params.get('slug') or 'None'
        data = DigiKalaData.get_sections(slug)
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status_request)


class GetSectionByLinkView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = GetUrlSrializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = DigiKalaData.get_section_by_link(url=serializer.data.get('url'))
        status_request = data.get('status', status.HTTP_200_OK)

        print(serializer.data)
        return Response(
            data,
            status = status_request
        )
