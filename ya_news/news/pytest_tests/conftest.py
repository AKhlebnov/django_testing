"""Доплнительные фикстуры pytest."""
from datetime import datetime, timedelta
from django.urls import reverse

import pytest
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


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
def news():
    return News.objects.create(
        title='Новость',
        text='Просто текст'
    )


@pytest.fixture
def news_list(admin_user):
    """Фикстура списка новостей."""
    today = datetime.today()
    news_list = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(news_list)


@pytest.fixture
def comment(author, news):
    """Фикстура комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comment_list(author, news):
    """Фикстура списка комментариев."""
    now = timezone.now()
    comment_list = []
    for index in range(2):
        comment_item = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}'
        )
        comment_item.created = now + timedelta(days=index)
        comment_item.save()
        comment_list.append(comment_item)
    return comment_list


@pytest.fixture
def url_detail(news):
    """Фикстура страницы новости"""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_home(news_list):
    """Фикстура главной страницы"""
    return reverse('news:home')


@pytest.fixture
def url_edit(comment):
    """Фикстура страницы редактирования комментария"""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete(comment):
    """Фикстура страницы удаления комментария"""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_login():
    """Фикстура страницы логина"""
    return reverse('users:login')


@pytest.fixture
def url_logout():
    """Фикстура страницы логаута"""
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    """Фикстура страницы регистрации"""
    return reverse('users:signup')
