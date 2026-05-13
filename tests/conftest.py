import pytest

from py_canada_post.client import PyCanadaPost

get_client = PyCanadaPost.from_env()


@pytest.fixture
def client():
    """
    Initialize reusable fixture to use in methods and classes without defining it.
    """

    return get_client
