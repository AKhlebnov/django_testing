"""Тестрирование маршрутов."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('id_news_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    ),
)
def test_home_availability_for_anonymous_user(client, name, args):
    """Тест главной страницы, новости, логина, логаута и регистрации."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, name, id_comment_for_args, expected_status
):
    """
    Тест доступа автора и другого пользователя к страницам
    редактирования и удаления комментариев.

    """
    url = reverse(name, args=id_comment_for_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirect_for_anonymous_client(client, name, id_comment_for_args):
    """
    Тест на редирект анонимного пользователя
    со страниц редактирования и удаления.

    """
    login_url = reverse('users:login')
    url = reverse(name, args=id_comment_for_args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
