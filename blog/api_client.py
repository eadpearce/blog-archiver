import requests
from urllib.parse import urlencode
from django.conf import settings


DEFAULT_PARAMS = {"api_key": settings.CONSUMER_KEY, "npf": True}
BASE_URL = 'https://api.tumblr.com/v2/blog/'
ENDPOINTS = {
    'info': '/info',
}


def get_blog_info(
    blog_name=None,
    **kwargs
):
    params = {
        **DEFAULT_PARAMS,
        **kwargs,
    }
    endpoint = ENDPOINTS['info']
    url = f"{BASE_URL}{blog_name}.tumblr.com{endpoint}?{urlencode(params)}"
    response = requests.get(url)
    return response.json(), response.status_code
