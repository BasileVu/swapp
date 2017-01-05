import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from comments.models import Comment
from items.models import Item, Category


class CommentsTests(TestCase):
    comments_url = "/api/comments/"
    comment1_url = "%s%d/" % (comments_url, 1)

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password")
        self.client.login(username="user1", password="password")

        self.category = Category.objects.create(name="category")
        self.item1 = Item.objects.create(name="test1", description="test", price_min=50, price_max=60,
                                         creation_date=timezone.now(), archived=False, owner=self.user,
                                         category=self.category)

    def create_comment(self, user, item, content="test", date=timezone.now()):
        Comment.objects.create(content=content, user=user, item=item, date=date)

    def check_get_comment_data_complete(self, data, comment_id=1, content="test"):
        self.assertEqual(data["id"], comment_id)
        self.assertEqual(data["content"], content)
        self.assertIn("date", data)
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["item"], self.item1.id)

    def test_post_comment(self):
        r = self.client.post(self.comments_url, data=json.dumps({
            "content": "test",
            "item": self.item1.id
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_get_comments(self):
        self.create_comment(self.user, self.item1)
        self.create_comment(self.user, self.item1, "other test")

        r = self.client.get(self.comments_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_comment_data_complete(r.data[0])
        self.check_get_comment_data_complete(r.data[1], 2, "other test")

    def test_get_comment(self):
        self.create_comment(self.user, self.item1)

        r = self.client.get(self.comment1_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_comment_data_complete(r.data)

    def test_get_only_own_comments(self):
        other_user = User.objects.create_user(username="user2", password="password")

        self.create_comment(self.user, self.item1, "comment user1")
        self.create_comment(other_user, self.item1, "comment user2")

        r = self.client.get(self.comments_url)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["content"], "comment user1")

    def test_get_comments_order_by_date(self):
        now = timezone.now()

        self.create_comment(self.user, self.item1, "test1", now + timezone.timedelta(seconds=4))
        self.create_comment(self.user, self.item1, "test2", now + timezone.timedelta(seconds=2))
        self.create_comment(self.user, self.item1, "test3", now + timezone.timedelta(seconds=3))

        r = self.client.get(self.comments_url)
        self.assertEquals(r.data[0]["content"], "test1")
        self.assertEquals(r.data[1]["content"], "test3")
        self.assertEquals(r.data[2]["content"], "test2")

    def test_put_comment(self):
        self.item2 = Item.objects.create(name="test2", description="test", price_min=50, price_max=60,
                                         creation_date=timezone.now(), archived=False, owner=self.user,
                                         category=self.category)
        self.create_comment(self.user, self.item1)

        r = self.client.put(self.comment1_url, data=json.dumps({
            "content": "put test",
            "item": self.item2.id
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.comment1_url)
        self.assertEqual(r.data["content"], "put test")
        self.assertEqual(r.data["item"], self.item2.id)

    def test_patch_comment(self):
        self.create_comment(self.user, self.item1)

        r = self.client.patch(self.comment1_url, data=json.dumps({
            "content": "patch test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.comment1_url)
        self.assertEqual(r.data["content"], "patch test")

    def test_delete_comment(self):
        self.create_comment(self.user, self.item1)

        r = self.client.delete(self.comment1_url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.client.get(self.comments_url)
        self.assertEqual(len(r.data), 0)
