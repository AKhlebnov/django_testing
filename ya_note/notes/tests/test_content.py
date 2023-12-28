"""Модуль с тестами для контента заметок."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestList(TestCase):
    """Контента списка."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Просто текст.',
            slug='slug',
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        """
        Тест отдельной заметки у автора
        или другого пользователя в списке.
        """
        users_statuses = (
            (self.author, True),
            (self.reader, False),
        )
        for user, note_in_list in users_statuses:
            self.client.force_login(user)
            url = reverse('notes:list')
            response = self.client.get(url)
            object_list = response.context['object_list']
            if note_in_list:
                self.assertIn(self.note, object_list)
            else:
                self.assertNotIn(self.note, object_list)


class TestDetailPage(TestCase):
    """Контент заметки."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Просто текст.',
            slug='slug',
            author=cls.author
        )

    def test_detail_note(self):
        """Тест на отображение содержимого заметки."""
        self.client.force_login(self.author)
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.text)

    def test_authorized_client_has_form(self):
        """Тест отображения формы заметки у авторизированного пользователя."""
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
