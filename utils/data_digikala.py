import requests
from rest_framework import status


class DigiKalaData:
    url_chapters = 'https://about.digikala.com/api/v1/dsb/report1401/chapters/'

    def get_data(self, url):
        try:
            response = requests.get(url)

            # Raise an error when the status response is not 200
            response.raise_for_status()

            return response.json()

        except requests.ConnectionError as error:
            return {
                'detail': "A network-related error occurred",
                'status': status.HTTP_503_SERVICE_UNAVAILABLE
            }

        except requests.Timeout as error:
            return {
                'detail': "A timeout occurred:",
                'status': status.HTTP_504_GATEWAY_TIMEOUT
            }

        except requests.HTTPError as error:
            return {
                'detail': error.response.reason,
                'status': error.response.status_code
            }
        except Exception as error:
            return {
                'detail': "An error occurred please try again !",
                'status': status.HTTP_400_BAD_REQUEST
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
