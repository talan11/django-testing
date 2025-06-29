from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.models import Comment

pytestmark = pytest.mark.django_db

FORM_COMMENT_DATA = {
    'text': 'Пример комментария'
}


def test_anonymous_user_cant_create_comment(client, news, url_detail):
    initial_comments = sorted(Comment.objects.values_list(
        'id', flat=True)
    )

    response = client.post(url_detail, data=FORM_COMMENT_DATA)
    final_comments = sorted(Comment.objects.values_list('id', flat=True))

    assert response.status_code == HTTPStatus.FOUND
    assert final_comments == initial_comments


def test_user_can_create_comment(
        author_client, author, news, url_detail
):
    Comment.objects.all().delete()
    author_client.post(url_detail, data=FORM_COMMENT_DATA)

    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == FORM_COMMENT_DATA['text']
    assert comment.news == news

    assert comment.author == author


def test_author_can_delete_comment(
        author_client, news, comment, url_delete, expected_url_detail_comments
):
    initial_comments_count = Comment.objects.count()
    response = author_client.delete(url_delete)
    assertRedirects(response, expected_url_detail_comments)
    assert not Comment.objects.filter(id=comment.id).exists()
    assert Comment.objects.count() == initial_comments_count - 1


def test_user_cant_delete_comment_of_another_user(
        news, admin_client, comment, url_delete
):
    response = admin_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(id=comment.id).exists()
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news
    assert new_comment.text == comment.text


def test_author_can_edit_comment(
        author_client, comment, news, url_edit, expected_url_detail_comments
):
    response = author_client.post(url_edit, data=FORM_COMMENT_DATA)
    assertRedirects(response, expected_url_detail_comments)
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.text == FORM_COMMENT_DATA['text']
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news


def test_not_author_cant_edit_comment(
        admin_client, comment, news, url_edit):
    response = admin_client.post(url_edit, data=FORM_COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    new_comment = Comment.objects.get(id=news.id)
    assert comment.text == new_comment.text
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news
