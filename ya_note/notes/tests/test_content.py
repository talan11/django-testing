from notes.forms import NoteForm
from .core.core_test_case import (
    CoreTestCase, URL_LIST, URL_ADD, URL_EDIT
)
from notes.models import Note


class TestNoteContent(CoreTestCase):
    def test_note_appears_in_authors_list(self):
        response = self.author_client.get(URL_LIST)
        notes_list = response.context["object_list"]

        self.assertIn(self.note, notes_list)

        note_from_list = notes_list.get(id=self.note.id)
        self.assertEqual(note_from_list.title, self.note.title)
        self.assertEqual(note_from_list.text, self.note.text)
        self.assertEqual(note_from_list.author, self.note.author)
        self.assertEqual(note_from_list.slug, self.note.slug)

    def test_forms_on_pages(self):
        form_pages = (URL_ADD, URL_EDIT)

        for url in form_pages:
            with self.subTest(url=url):
                response = self.author_client.get(url)

                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)

                # Получаем количество заметок в базе данных
                total_notes_in_db = Note.objects.count()
                # Получаем заметки на странице
                notes_list_on_page = response.context["object_list"]

                # Проверка единственности записи на странице
                self.assertEqual(len(notes_list_on_page), total_notes_in_db)

    def test_note_not_in_list_for_other_users(self):
        response = self.reader_client.get(URL_LIST)
        self.assertNotIn(self.note, response.context["object_list"])

    def test_forms_on_pages(self):
        form_pages = (URL_ADD, URL_EDIT)

        for url in form_pages:
            with self.subTest(url=url):
                response = self.author_client.get(url)

                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
