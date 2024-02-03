import requests
from requests.exceptions import HTTPError


class DigiKalaData:
    url_chapters = 'https://about.digikala.com/api/v1/dsb/report1401/chapters/'

    def get_data(self, url):
        try:
            response = requests.get(url)
            return response.json()

        except Exception as error:
            if isinstance(error, HTTPError):
                return {'detail': error.response.reason}
            else:
                return {'detail': 'error request .'}

    def get_chapters(self):
        response = self.get_data(self.url_chapters)
        if response.get('results'):
            response = {'chapters': response.get('results')}
        return response
