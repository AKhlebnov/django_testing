"""Модуль с тестами логики приложения."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

User = get_user_model()


class TestNoteCreation(TestCase):
    """Тест откправки заметки и проверки содержимого slug."""

    NOTE_TITLE = 'Новая заметка'
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст заметки',
            slug='slug_text',
            author=cls.user
        )
        cls.url = reverse('notes:add', None)
        cls.url_success = reverse('notes:success', None)
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.anonymous_client = Client()
        cls.form_data = {'title': cls.NOTE_TITLE, 'text': cls.NOTE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        """Тест создания заметки анонимным пользователем."""
        self.anonymous_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_user_can_create_note(self):
        """Тест создания заметки авторизированным пользователем."""
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)
        note = Note.objects.get(pk=2)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)

    def test_user_cant_use_non_unique_slug(self):
        """Тест на уникальность поля slug."""
        non_unique_slug_data = {
            'title': 'Заметка',
            'text': 'Текст заметки',
            'slug': self.note.slug,
            'author': self.user
        }
        response = self.auth_client.post(self.url, data=non_unique_slug_data)
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
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.latest('id')
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(TestCase):
    """
    Тест на редактирование и удаления заметки
    авторизированным пользователем и другим пользователем.
    """

    NOTE_TITLE = 'Заметка'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug_text'
    NEW_NOTE_TEXT = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.another_author = User.objects.create(username='Другой автор')
        cls.another_author_client = Client()
        cls.another_author_client.force_login(cls.another_author)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author
        )
        cls.success_url = reverse('notes:success', None)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'title': cls.NOTE_TITLE, 'text': cls.NEW_NOTE_TEXT}

    def test_author_can_delete_note(self):
        """Тест на удаление автором своей заметки."""
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        """Тест на удаление чужой заметки."""
        response = self.another_author_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_author_can_edit_note(self):
        """Тест на редактирование заметки автором."""
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        """Тест на редактирование чужой заметки."""
        response = self.another_author_client.post(
            self.edit_url,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
