"""Модуль фикстур"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class BaseNotesTestCase(TestCase):
    """Базовый класс для тестов контента"""

    NOTE_TITLE = 'Заметка'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = 'slug_text'
    NEW_NOTE_TITLE = 'Новая заметка'
    NEW_NOTE_TEXT = 'Новый текст заметки'
    AUTHOR_USERNAME = 'Лев Толстой'
    ANOTHER_AUTHOR_USERNAME = 'Другой автор'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=cls.AUTHOR_USERNAME)
        cls.another_author = User.objects.create(
            username=cls.ANOTHER_AUTHOR_USERNAME
        )
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author
        )
        cls.anonymous_client = Client()
        cls.url_list = reverse('notes:list')
        cls.url_detail = reverse('notes:detail', args=(cls.note.slug,))
        cls.url_add = reverse('notes:add')
        cls.url_success = reverse('notes:success')
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.url_home = reverse('notes:home')
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_signup = reverse('users:signup')
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE, 'text': cls.NEW_NOTE_TEXT
        }
