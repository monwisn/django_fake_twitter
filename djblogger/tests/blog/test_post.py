import pytest
from django.urls import reverse
from enum import Enum
from http import HTTPStatus

pytestmark = pytest.mark.django_db


class Status(Enum):
    OK = 200
    # OK = HTTPStatus.OK
    BAD_GATEWAY = 502
    # BAD_GATEWAY = HTTPStatus.BAD_GATEWAY
    FORBIDDEN = 403
    # FORBIDDEN = HTTPStatus.FORBIDDEN
    TOO_MANY_REQUESTS = 429
    # TOO_MANY_REQUESTS = HTTPStatus.TOO_MANY_REQUESTS


status = Status.OK

if status == Status.OK:
    print('OK')


class TestPostSingle:
    def test_post_single_url(self, client, post_factory):
        post = post_factory()
        url = reverse('post_single', kwargs={'post': post.slug})
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
