import requests
from urllib.parse import urlencode
from django.conf import settings


DEFAULT_PARAMS = {"api_key": settings.CONSUMER_KEY, "npf": True}
BASE_URL = 'https://api.tumblr.com/v2/blog/'
ENDPOINTS = {
    'info': '/info',
    'posts': '/posts',
}


def build_url(blog_name, endpoint, params):
    return f"{BASE_URL}{blog_name}.tumblr.com{endpoint}?{urlencode(params)}"


def get_blog_info(
    blog_name=None,
    **kwargs
):
    params = {
        **DEFAULT_PARAMS,
        **kwargs,
    }
    endpoint = ENDPOINTS['info']
    url = build_url(blog_name, endpoint, params)
    response = requests.get(url)
    return response.json(), response.status_code


def get_posts(
    blog_name=None,
    **kwargs
):
    params = {
        **DEFAULT_PARAMS,
        **kwargs,
    }
    endpoint = ENDPOINTS['posts']
    url = build_url(blog_name, endpoint, params)
    response = requests.get(url)
    return response.json(), response.status_code
