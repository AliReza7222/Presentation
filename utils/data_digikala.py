import requests

from rest_framework import status


class DigiKalaData:
    URL_DIGIKALA = 'https://about.digikala.com/api/v1/dsb/report1401/chapters'

    @staticmethod
    def get_data(url: str) -> dict:
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

    @classmethod
    def get_chapters(cls) -> dict:
        response = cls.get_data(cls.URL_DIGIKALA)
        if results := response.get('results'):
            response = {'data': results}
        return response

    @classmethod
    def get_sections(cls, slug: str) -> dict:
        url = '/'.join([cls.URL_DIGIKALA, slug])
        response = cls.get_data(url)
        if sections := response.get('sections'):
            response = {'data': sections}
        return response

    @classmethod
    def get_section_by_link(cls, url: str) -> dict:
        split_url = url.split('/')

        if not '/'.join(split_url[:-2]) == cls.URL_DIGIKALA:
            return {'detail': 'NotFound', 'status': status.HTTP_404_NOT_FOUND}

        slug, html_id = split_url[-2], split_url[-1].lstrip('#')
        response = cls.get_sections(slug)

        if sections := response.get('data'):
            for section in sections:
                if section.get('html_id') == html_id:
                    return {'data': section}
            return {'detail': 'Invalid html_id !', 'status': status.HTTP_400_BAD_REQUEST}
        return response
