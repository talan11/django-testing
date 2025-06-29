from http import HTTPStatus

from .core.core_test_case import (
    CoreTestCase,
    URL_HOME, URL_LOGIN, URL_LOGOUT, URL_SIGNUP, URL_ADD,
    URL_LIST, URL_SUCCESS, URL_DETAIL, URL_EDIT, URL_DELETE,
    URL_LIST_WITH_NEXT, URL_SUCCESS_WITH_NEXT, URL_ADD_WITH_NEXT,
    URL_DETAIL_WITH_NEXT, URL_EDIT_WITH_NEXT, URL_DELETE_WITH_NEXT,
)


class TestRoutesAvailability(CoreTestCase):
    def test_pages_availability_for_different_users(self):
        test_cases = [
            # Доступность страниц для анонимных пользователей
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),

            # Доступность страниц для авторизованных пользователей
            (URL_ADD, self.reader_client, HTTPStatus.OK),
            (URL_LIST, self.reader_client, HTTPStatus.OK),
            (URL_SUCCESS, self.reader_client, HTTPStatus.OK),

            # Доступность страниц для автора заметки
            (URL_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_EDIT, self.author_client, HTTPStatus.OK),
            (URL_DELETE, self.author_client, HTTPStatus.OK),

            # Ограничение доступа для не-авторов
            (URL_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (URL_EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),

            # Перенаправления для анонимов
            (URL_ADD, self.client, HTTPStatus.FOUND),
            (URL_LIST, self.client, HTTPStatus.FOUND),
            (URL_SUCCESS, self.client, HTTPStatus.FOUND),
            (URL_DETAIL, self.client, HTTPStatus.FOUND),
            (URL_EDIT, self.client, HTTPStatus.FOUND),
            (URL_DELETE, self.client, HTTPStatus.FOUND),
        ]

        for url, client, expected_status in test_cases:
            with self.subTest(url=url, client=client):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous_users(self):
        redirect_test_cases = [
            (URL_LIST, URL_LIST_WITH_NEXT),
            (URL_SUCCESS, URL_SUCCESS_WITH_NEXT),
            (URL_ADD, URL_ADD_WITH_NEXT),
            (URL_DETAIL, URL_DETAIL_WITH_NEXT),
            (URL_EDIT, URL_EDIT_WITH_NEXT),
            (URL_DELETE, URL_DELETE_WITH_NEXT),
        ]

        for url, expected_redirect in redirect_test_cases:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
