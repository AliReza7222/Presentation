from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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
        data = DigiKalaData.get_section(slug)
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status_request)
