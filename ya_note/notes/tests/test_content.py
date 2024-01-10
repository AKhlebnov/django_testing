"""Модуль с тестами для контента заметок."""

from .test_utils import BaseNotesTestCase


class TestNotesList(BaseNotesTestCase):
    """Контента списка заметок."""

    def test_notes_list_for_different_users(self):
        """
        Тест отдельной заметки у автора
        или другого пользователя в списке.
        """
        users_statuses = (
            (self.author, True),
            (self.another_author, False),
        )
        for user, note_in_list in users_statuses:
            self.client.force_login(user)

            response = self.client.get(self.url_list)
            object_list = response.context['object_list']
            if note_in_list:
                self.assertIn(self.note, object_list)
            else:
                self.assertNotIn(self.note, object_list)


class TestDetailPage(BaseNotesTestCase):
    """Контент отдельной заметки."""

    def test_detail_note(self):
        """Тест на отображение содержимого заметки."""
        self.client.force_login(self.author)
        response = self.client.get(self.url_detail)
        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.text)

    def test_authorized_client_has_form(self):
        """Тест отображения формы заметки у авторизированного пользователя."""
        urls = (
            self.url_add,
            self.url_edit,
        )
        self.client.force_login(self.author)
        for url in urls:
            with self.subTest(name=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
