"""Модуль для тестрирования маршрутов."""
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_home'),
        pytest.lazy_fixture('url_login'),
        pytest.lazy_fixture('url_logout'),
        pytest.lazy_fixture('url_signup')
    ),
)
def test_home_availability_for_anonymous_user(client, url):
    """Тест главной страницы, новости, логина, логаута и регистрации."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_availability_for_anonymous_user(client, url_detail):
    """
    Тест доступности страницы деталей
    новости для анонимного пользователя.
    """
    response = client.get(url_detail)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_edit'), pytest.lazy_fixture('url_delete')),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, url, expected_status
):
    """
    Тест доступа автора и другого пользователя к страницам
    редактирования и удаления комментариев.

    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_edit'), pytest.lazy_fixture('url_delete')),
)
def test_redirect_for_anonymous_client(client, url, url_login):
    """
    Тест на редирект анонимного пользователя
    со страниц редактирования и удаления.

    """
    expected_url = f'{url_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
