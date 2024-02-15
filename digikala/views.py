from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from utils.data_digikala import DigiKalaData


class GetChaptersView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        data = DigiKalaData.get_chapters()
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status=status_request)


class GetSectionView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        slug = kwargs.get('slug') or 'None'
        data = DigiKalaData.get_section(slug)
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status_request)
