from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db

URL_HOME = lazy_fixture('url_home')
URL_SIGNUP = lazy_fixture('url_signup')
URL_LOGIN = lazy_fixture('url_login')
URL_LOGOUT = lazy_fixture('url_logout')
URL_DETAIL = lazy_fixture('url_detail')
URL_EDIT = lazy_fixture('url_edit')
URL_DELETE = lazy_fixture('url_delete')
EXPECTED_URL_EDIT = pytest.lazy_fixture('expected_url_edit')
EXPECTED_URL_DELETE = pytest.lazy_fixture('expected_url_delete')
CLIENT = lazy_fixture('client')
AUTHOR_CLIENT = lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    (
        (URL_HOME, CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, CLIENT, HTTPStatus.OK),
        (URL_LOGIN, CLIENT, HTTPStatus.OK),
        (URL_DETAIL, CLIENT, HTTPStatus.OK),
        (URL_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DELETE, AUTHOR_CLIENT, HTTPStatus.OK),

        (URL_EDIT, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_DELETE, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),

        (URL_EDIT, CLIENT, HTTPStatus.FOUND),
        (URL_DELETE, CLIENT, HTTPStatus.FOUND),
    )
)
def test_pages_availability(
        reverse_url, parametrized_client, expected_status
):
    assert parametrized_client.get(reverse_url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    [
        (URL_EDIT, EXPECTED_URL_EDIT),
        (URL_DELETE, EXPECTED_URL_DELETE),
    ],
)
def test_redirect_for_anonymous_client(
        client, url, expected_url
):
    assertRedirects(client.get(url), expected_url)
