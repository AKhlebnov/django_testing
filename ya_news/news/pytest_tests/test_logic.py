"""Модуль тестов логики приложения."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import INDEX_NUMBER


def test_user_can_create_comment(
        author_client, author,
        form_data,
        id_news_for_args
):
    """Тест пользователь может создать комментарий."""
    url = reverse('news:detail', args=id_news_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.author == author
    assert new_comment.text == form_data['text']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, form_data,
        id_news_for_args
):
    """Тест аноним не может создать комментарий."""
    url = reverse('news:detail', args=id_news_for_args)
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_use_bad_words(author_client, form_data, id_news_for_args):
    """Тест проверка запрещённых слов."""
    bad_words_data = f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    url = reverse('news:detail', args=id_news_for_args)
    form_data['text'] = bad_words_data
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_note(
        author_client,
        form_data,
        comment_list,
        id_news_for_args,
        id_comment_for_args
):
    """Тест пользователь может редактировать комментарий."""
    url = reverse('news:edit', args=id_comment_for_args)
    url_comments = reverse('news:detail', args=id_news_for_args)
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{url_comments}#comments')
    comment_list[INDEX_NUMBER].refresh_from_db()
    assert comment_list[INDEX_NUMBER].text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
        admin_client,
        form_data,
        comment_list,
        id_comment_for_args
):
    """Тест пользователь не может редактировать чужой комментарий."""
    url = reverse('news:edit', args=id_comment_for_args)
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Comment.objects.get(id=comment_list[0].id)
    assert comment_list[INDEX_NUMBER].text == note_from_db.text


def test_author_can_delete_comment(
        author_client,
        id_news_for_args,
        id_comment_for_args
):
    """Тест автор может удалить свой комментарий."""
    url = reverse('news:delete', args=id_comment_for_args)
    url_comments = reverse('news:detail', args=id_news_for_args)
    response = author_client.post(url)
    assertRedirects(response, f'{url_comments}#comments')
    assert Comment.objects.count() == 1


def test_user_cant_delete_comment_of_another_user(
        admin_client,
        id_comment_for_args
):
    """Тест пользователь не может удалить чужой комментарий."""
    url = reverse('news:delete', args=id_comment_for_args)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 2
