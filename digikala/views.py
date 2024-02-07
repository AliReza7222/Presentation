from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from utils.data_digikala import DigiKalaData


class GetChaptersView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        object_digikala_data = DigiKalaData()
        data = object_digikala_data.get_chapters()
        status_response = object_digikala_data.check_status(data)
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status=status_request)


class GetSectionView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        object_digikala_data = DigiKalaData()
        slug = request.query_params.get('slug') or 'None'
        data = object_digikala_data.get_section(slug)
        status_request = data.get('status', status.HTTP_200_OK)
        return Response(data, status_request)