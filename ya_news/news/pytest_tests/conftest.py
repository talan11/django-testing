from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Какой то заголовок',
        text='пример текста',
        date=timezone.now(),
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text='Какой то комментарий',
        news=news,
        author=author
    )
    return comment


@pytest.fixture
def list_news():
    today = datetime.today()
    News.objects.bulk_create(
        News(title=f'Новость номер {index}',
             text='Какой то текст',
             date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def list_comments(news, author):
    now = datetime.now()
    for index in range(10):
        comment = Comment(
            news=news,
            author=author,
            text=f'Какой то текст номер {index}',
            created=now + timedelta(index)
        )
        comment.save()


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def expected_url_detail(url_login, url_detail):
    return f'{url_login}?next={url_detail}'


@pytest.fixture
def expected_url_edit(url_login, url_edit):
    return f'{url_login}?next={url_edit}'


@pytest.fixture
def expected_url_delete(url_login, url_delete):
    return f'{url_login}?next={url_delete}'


@pytest.fixture
def expected_url_detail_comments(url_detail):
    return f"{url_detail}#comments"
