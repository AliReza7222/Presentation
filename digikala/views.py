from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from utils.data_digikala import DigiKalaData


class GetChaptersView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        object_digikala_data = DigiKalaData()
        data = object_digikala_data.get_chapters()
        status_response = status.HTTP_200_OK

        if data.get('detail'):
            status_response = status.HTTP_400_BAD_REQUEST

        return Response(data, status=status_response)
