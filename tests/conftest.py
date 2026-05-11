import pytest

from py_canada_post.client import PyCanadaPost

get_client = PyCanadaPost.from_env()

@pytest.fixture
def client():
    return get_client
