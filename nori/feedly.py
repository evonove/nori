import requests


FEEDLY_BASE_URL = 'http://cloud.feedly.com'
FEEDLY_API_VERSION = 'v3'


class FeedlyError(Exception):
    """
    Exception raised when feedly API returns non-200 status code.

    Attributes:
        status -- the status code returned by the feedly api
        content -- a description of the error
    """
    def __init__(self, status, content):
        self.status = status
        self.content = content


class Feedly:
    def __init__(self, token):
        self._api_root = '%s/%s' % (FEEDLY_BASE_URL, FEEDLY_API_VERSION)

        # create the authorization header used to authenticate the requests
        self._headers = {'Authorization': 'OAuth %s' % token}

    def get_categories(self):
        url = '%s/categories' % self._api_root
        response = requests.get(url, headers=self._headers)
        if response.status_code != requests.codes.ok:
            raise FeedlyError(response.status_code, response.content)

        return response.json()

    def get_streams_contents(self, stream_id, count=20, newer_than=None):
        params = {'streamId': stream_id, 'count': count}
        if newer_than is not None:
            params.update({'newerThan': newer_than})

        url = '%s/streams/contents' % self._api_root
        response = requests.get(url, params=params, headers=self._headers)
        if response.status_code != requests.codes.ok:
            raise FeedlyError(response.status_code, response.content)

        return response.json()
