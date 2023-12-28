"""Доплнительные фикстуры pytest."""
from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News

INDEX_NUMBER = 0


@pytest.fixture
def author(django_user_model):
    """Модель пользователя django_user_model."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def anonymous_client(client):
    """Фикстура создания анонимного."""
    return client


@pytest.fixture
def author_client(author, client):
    """Фикстура вызова клиента и автора."""
    client.force_login(author)
    return client


@pytest.fixture
def news_list(db):
    """Фикстура списка новостей."""
    today = datetime.today()
    news_list = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_item = News.objects.create(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        news_list.append(news_item)
    return news_list


@pytest.fixture
def id_news_for_args(news_list):
    """Фикстура id новости."""
    return news_list[INDEX_NUMBER].id,


@pytest.fixture
def comment_list(author, news_list):
    """Фикстура списка комментариев."""
    now = timezone.now()
    comment_list = []
    for index in range(2):
        comment_item = Comment.objects.create(
            news=news_list[INDEX_NUMBER],
            author=author,
            text=f'Текст {index}'
        )
        comment_item.created = now + timedelta(days=index)
        comment_item.save()
        comment_list.append(comment_item)
    return comment_list


@pytest.fixture
def id_comment_for_args(comment_list):
    """Фикстура id новости."""
    return comment_list[INDEX_NUMBER].id,


@pytest.fixture
def form_data():
    """Фикстура данных для формы комментария."""
    return {
        'text': 'Новый комментарий'
    }
