"""Модуль для тест контента."""
import pytest
from django.conf import settings
from django.urls import reverse


def test_news_count(client, news_list):
    """Тест проверки количества новостей на главной странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list):
    """Тест сортировки новостей на главной странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, comment_list, id_news_for_args):
    """Тест на сортировку комментариев новости."""
    url = reverse('news:detail', args=id_news_for_args)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, form_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('anonymous_client'), False),
    )
)
def test_authorized_anonymous_clienthas_has(
    parametrized_client, form_in_list, id_news_for_args
):
    """Тест проверки формы у авторизированного пользователя и анонима."""
    url = reverse('news:detail', args=id_news_for_args)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_list
