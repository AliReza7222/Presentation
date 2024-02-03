import requests
from requests.exceptions import HTTPError


class DigiKalaData:
    url_chapters = 'https://about.digikala.com/api/v1/dsb/report1401/chapters/'

    def get_data(self, url):
        try:
            response = requests.get(url)

            return response.json()

        except HTTPError:
            return f'Http error : {response.reason}'

    def get_specifications_data(self):
        specifications_data = self.get_data(self.url_chapters)
        del specifications_data['results']
        return specifications_data

    def get_chapters(self):
        chapters = {
            'chapters': self.get_data(self.url_chapters).get('results')
        }
        return chapters
