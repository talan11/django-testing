from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

URL_HOME = reverse('notes:home')
URL_LIST = reverse('notes:list')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_SUCCESS = reverse('notes:success')
URL_ADD = reverse('notes:add')

URL_LIST_WITH_NEXT = f'{URL_LOGIN}?next={URL_LIST}'
URL_SUCCESS_WITH_NEXT = f'{URL_LOGIN}?next={URL_SUCCESS}'
URL_ADD_WITH_NEXT = f'{URL_LOGIN}?next={URL_ADD}'

DUMMY_SLUG = 'myslug'

URL_DETAIL = reverse('notes:detail', args=(DUMMY_SLUG,))
URL_EDIT = reverse('notes:edit', args=(DUMMY_SLUG,))
URL_DELETE = reverse('notes:delete', args=(DUMMY_SLUG,))

URL_DETAIL_WITH_NEXT = f'{URL_LOGIN}?next={URL_DETAIL}'
URL_EDIT_WITH_NEXT = f'{URL_LOGIN}?next={URL_EDIT}'
URL_DELETE_WITH_NEXT = f'{URL_LOGIN}?next={URL_DELETE}'


class CoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='my title',
            text='my text',
            author=cls.author,
            slug=DUMMY_SLUG
        )

        cls.form_data_post = {
            'title': 'Fmy title',
            'text': 'Fmy text',
            'slug': 'Fmyslug',
        }
