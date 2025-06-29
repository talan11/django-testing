import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(
        client, list_news, url_home
):
    assert client.get(
        url_home
    ).context[
        'object_list'
    ].count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_comments_order(
        news, client, list_comments, url_detail
):
    response = client.get(url_detail)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    timestamps = [
        i.created for i in all_comments
    ]
    assert timestamps == sorted(timestamps)


def test_news_order(
        client, list_news, url_home
):
    news = [
        i.date for i in client.get(url_home).context['object_list']
    ]
    assert news == sorted(news, reverse=True)


def test_authorized_user_has_comment_form(
        author_client, comment, url_detail
):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_unauthorized_user_does_not_have_comment_form(
        client, comment, url_detail
):
    assert 'form' not in client.get(url_detail).context
