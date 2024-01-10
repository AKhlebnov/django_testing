"""Модуль с тестами логики приложения."""

from http import HTTPStatus

from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify
from .test_utils import BaseNotesTestCase


class TestNoteCreation(BaseNotesTestCase):
    """Тест откправки заметки и проверки содержимого slug."""

    def test_anonymous_user_cant_create_note(self):
        """Тест создания заметки анонимным пользователем."""
        Note.objects.all().delete()
        self.anonymous_client.post(self.url_add, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        """Тест создания заметки авторизированным пользователем."""
        self.client.force_login(self.author)
        response = self.client.post(self.url_add, data=self.form_data)

        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)
        note = Note.objects.get(pk=2)
        self.assertEqual(note.title, self.NEW_NOTE_TITLE)
        self.assertEqual(note.text, self.NEW_NOTE_TEXT)
        self.assertEqual(note.author, self.author)

    def test_user_cant_use_non_unique_slug(self):
        """Тест на уникальность поля slug."""
        non_unique_slug_data = {
            'title': 'Заметка',
            'text': 'Текст заметки',
            'slug': self.note.slug,
            'author': self.author
        }
        self.client.force_login(self.author)
        response = self.client.post(self.url_add, data=non_unique_slug_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=[f'{self.note.slug}{WARNING}']
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug(self):
        """Тест автоматического добавления slug."""
        self.client.force_login(self.author)
        response = self.client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.latest('id')
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(BaseNotesTestCase):
    """
    Тест на редактирование и удаления заметки
    авторизированным пользователем и другим пользователем.
    """

    def test_author_can_delete_note(self):
        """Тест на удаление автором своей заметки."""
        self.client.force_login(self.author)
        response = self.client.delete(self.url_delete)
        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        """Тест на удаление чужой заметки."""
        self.client.force_login(self.another_author)
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_author_can_edit_note(self):
        """Тест на редактирование заметки автором."""
        self.client.force_login(self.author)
        response = self.client.post(self.url_edit, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        """Тест на редактирование чужой заметки."""
        self.client.force_login(self.another_author)
        response = self.client.post(self.url_edit, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
