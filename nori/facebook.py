import requests


FACEBOOK_BASE_URL = 'https://graph.facebook.com'
FACEBOOK_API_VERSION = 'v2.8'


class FacebookError(Exception):
    """
    Exception raised when facebook API returns non-200 status code.

    Attributes:
        status -- the status code returned by the facebook api
        content -- a description of the error
    """
    def __init__(self, status, content):
        self.status = status
        self.content = content


class Facebook:
    def __init__(self, token):
        self._api_root = '%s/%s' % (FACEBOOK_BASE_URL, FACEBOOK_API_VERSION)
        self._access_token = token

    def get_urls(self, *urls):
        """
        Returns a JSON with informations on the `url` as it releates
        with the Facebook Social Graph.

        ref: https://developers.facebook.com/docs/graph-api/reference/url/
        """
        params = {'ids': ','.join(urls), 'access_token': self._access_token}

        response = requests.get(self._api_root, params=params)
        if response.status_code != requests.codes.ok:
            raise FacebookError(response.status_code, response.content)

        return response.json()
