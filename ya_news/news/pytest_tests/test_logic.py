"""Модуль тестов логики приложения."""
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Какой-то текст'}


def test_user_can_create_comment(
        author_client, author,
        url_detail
):
    """Тест пользователь может создать комментарий."""
    assert Comment.objects.count() == 0
    response = author_client.post(url_detail, data=FORM_DATA)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.author == author
    assert new_comment.text == FORM_DATA['text']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client,
        url_detail
):
    """Тест аноним не может создать комментарий."""
    client.post(url_detail, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_use_bad_words(author_client, url_detail):
    """Тест проверка запрещённых слов."""
    form_data_copy = FORM_DATA.copy()
    bad_words_data = f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    form_data_copy['text'] = bad_words_data
    response = author_client.post(url_detail, data=form_data_copy)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client,
        comment,
        url_detail,
        url_edit
):
    """Тест пользователь может редактировать комментарий."""
    response = author_client.post(url_edit, FORM_DATA)
    assertRedirects(response, f'{url_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(
        admin_client,
        comment,
        url_edit
):
    """Тест пользователь не может редактировать чужой комментарий."""
    response = admin_client.post(url_edit, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
        author_client,
        url_detail,
        url_delete
):
    """Тест автор может удалить свой комментарий."""
    response = author_client.post(url_delete)
    assertRedirects(response, f'{url_detail}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        admin_client,
        url_delete
):
    """Тест пользователь не может удалить чужой комментарий."""
    response = admin_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
