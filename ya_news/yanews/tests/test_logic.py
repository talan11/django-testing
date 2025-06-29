from http import HTTPStatus

from pytils.translit import slugify

from .core.core_test_case import (
    CoreTestCase,
    URL_ADD,
    URL_SUCCESS,
    URL_EDIT,
    URL_DELETE
)
from news.forms import WARNING
from news.models import News


class TestRoutes(CoreTestCase):
    def assert_note_created_successfully(self, expected_slug_value=None):
        News.objects.all().delete()
        response = self.author_client.post(
            URL_ADD,
            data=self.form_data_post
        )
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(News.objects.count(), 1)
        created_note = News.objects.last()
        self.assertIsNotNone(created_note, "Заметка не была создана.")
        self.assertEqual(created_note.title, self.form_data_post["title"])
        self.assertEqual(created_note.text, self.form_data_post["text"])
        if expected_slug_value is None:
            expected_slug_value = slugify(self.form_data_post["title"])
        self.assertEqual(created_note.slug, expected_slug_value)
        self.assertEqual(created_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        initial_notes_ids = set(News.objects.values_list("id", flat=True))
        self.client.post(URL_ADD, data=self.form_data_post)
        self.assertEqual(
            initial_notes_ids,
            set(News.objects.values_list("id", flat=True))
        )

    def test_not_unique_slug(self):
        initial_notes_ids = set(News.objects.values_list("id", flat=True))

        self.form_data_post["slug"] = self.note.slug
        response = self.author_client.post(URL_ADD, data=self.form_data_post)
        self.assertEqual(
            initial_notes_ids,
            set(News.objects.values_list("id", flat=True))
        )
        self.assertFormError(
            response,
            "form",
            "slug",
            errors=(self.note.slug + WARNING)
        )

    def test_empty_slug(self):
        self.form_data_post.pop("slug")
        self.assert_note_created_successfully()

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data_post)

        self.assertRedirects(response, URL_SUCCESS)
        edited_note = News.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data_post["title"])
        self.assertEqual(edited_note.text, self.form_data_post["text"])
        self.assertEqual(edited_note.slug, self.form_data_post["slug"])
        self.assertEqual(edited_note.author, self.note.author)

    def test_not_author_cant_edit_note(self):
        response = self.reader_client.post(URL_EDIT, self.form_data_post)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        unchanged_note = News.objects.get(id=self.note.id)

        self.assertEqual(unchanged_note.title, self.note.title)
        self.assertEqual(unchanged_note.text, self.note.text)
        self.assertEqual(unchanged_note.slug, self.note.slug)
        self.assertEqual(unchanged_note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes_count_before = News.objects.count()
        response = self.author_client.post(URL_DELETE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(News.objects.count(), notes_count_before - 1)
        self.assertFalse(News.objects.filter(id=self.note.id).exists())

    def test_not_author_cant_delete_note(self):
        notes_count_before = News.objects.count()

        note_before_deletion = News.objects.get(id=self.note.id)

        response = self.reader_client.post(URL_DELETE)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(News.objects.count(), notes_count_before)
        self.assertTrue(News.objects.filter(id=self.note.id).exists())
        note_after_deletion = News.objects.get(id=self.note.id)

        self.assertEqual(note_before_deletion.title, note_after_deletion.title)
        self.assertEqual(note_before_deletion.text, note_after_deletion.text)
        self.assertEqual(note_before_deletion.author,
                         note_after_deletion.author)
