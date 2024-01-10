"""Модуль с тестами маршрутов."""

from http import HTTPStatus

from .test_utils import BaseNotesTestCase


class TestRoutes(BaseNotesTestCase):
    """Тесты адресов страниц."""

    def test_pages_availability(self):
        """Тест доступности страниц для разных пользователей."""
        cases = (
            (None, self.url_home, HTTPStatus.OK),
            (None, self.url_login, HTTPStatus.OK),
            (None, self.url_logout, HTTPStatus.OK),
            (None, self.url_signup, HTTPStatus.OK),
            (self.author, self.url_list, HTTPStatus.OK),
            (self.author, self.url_success, HTTPStatus.OK),
            (self.author, self.url_add, HTTPStatus.OK),
            (self.author, self.url_detail, HTTPStatus.OK),
            (self.author, self.url_edit, HTTPStatus.OK),
            (self.author, self.url_delete, HTTPStatus.OK),
            (self.another_author, self.url_detail, HTTPStatus.NOT_FOUND),
            (self.another_author, self.url_edit, HTTPStatus.NOT_FOUND),
            (self.another_author, self.url_delete, HTTPStatus.NOT_FOUND),
        )
        for user, url, status in cases:
            with self.subTest(user=user, url=url):
                if user:
                    self.client.force_login(user)

                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Тест редиректа неавторизованных пользователей."""
        urls = (
            self.url_detail,
            self.url_edit,
            self.url_delete,
            self.url_list,
            self.url_add,
            self.url_success,
        )
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
