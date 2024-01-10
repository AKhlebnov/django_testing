"""Модуль для тестов контента."""
import pytest
from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, url_home):
    """Тест проверки количества новостей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, url_home):
    """Тест сортировки новостей на главной странице."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, comment_list, url_detail):
    """Тест на сортировку комментариев новости."""
    response = client.get(url_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_authorized_client_has_form(author_client, url_detail):
    """Тест проверки формы у авторизованного пользователя"""
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_anonymous_client_has_form(anonymous_client, url_detail):
    """Тест проверки формы у анонимного пользователя"""
    response = anonymous_client.get(url_detail)
    assert 'form' not in response.context
