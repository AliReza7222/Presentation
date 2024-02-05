import requests
from rest_framework import status
from requests.exceptions import HTTPError


class DigiKalaData:
    url_chapters = 'https://about.digikala.com/api/v1/dsb/report1401/chapters/'

    def get_data(self, url):
        try:
            data = requests.get(url)

            if data.status_code == 404:
                response = {
                    'detail': f'Page {data.reason}',
                    'status': 404
                }
                return response

            return data.json()

        except Exception as error:
            if isinstance(error, HTTPError):
                return {'detail': error.response.reason}
            else:
                return {
                    'detail': 'request error to connect digikala !',
                    'status': 400
                }

    def get_chapters(self):
        response = self.get_data(self.url_chapters)
        if response.get('results'):
            response = {'chapters': response.get('results')}
        return response

    def get_section(self, slug):
        url_sction = self.url_chapters + slug
        response = self.get_data(url_sction)
        if response.get('sections'):
            response = {'sections': response.pop('sections')}
        return response

    def check_status(self, response):
        status_response = status.HTTP_200_OK
        status_code = response.pop('status', None)
        if status_code == 400:
            status_response = status.HTTP_400_BAD_REQUEST
        elif status_code == 404:
            status_response = status.HTTP_404_NOT_FOUND
        return status_response
