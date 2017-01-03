import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from items.models import Item, Category


class CommentsTests(TestCase):
    url_comments = "/api/comments/"
    url_comment1 = "%s/%d/" % (url_comments, 1)

    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")

        self.category = Category.objects.create(name="category")
        self.item1 = Item.objects.create(name="test1", description="test", price_min=50, price_max=60,
                                         creation_date=timezone.now(), archived=False, owner=self.user,
                                         category=self.category)

    def post_comment(self, item_id, content="test"):
        return self.client.post(self.url_comments, data=json.dumps({
            "content": content,
            "item": item_id
        }), content_type="application/json")

    def check_get_comment_data_complete(self, data):
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["content"], "test")
        self.assertIn("date", data)
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(data["item"], self.item1.id)

    def test_post_comment(self):
        r = self.post_comment(self.item1.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_get_comments(self):
        self.post_comment(self.item1.id)
        self.post_comment(self.item1.id, "other test")

        r = self.client.get(self.url_comments)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_comment_data_complete(r.data[0])
        self.check_get_comment_data_complete(r.data[1])

    def test_get_comment(self):
        self.post_comment(self.item1.id)

        r = self.client.get(self.url_comment1)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_comment_data_complete(r.data)

    def test_put_comment(self):
        self.item2 = Item.objects.create(name="test2", description="test", price_min=50, price_max=60,
                                         creation_date=timezone.now(), archived=False, owner=self.user,
                                         category=self.category)

        self.post_comment(self.item1.id)

        r = self.client.put(self.url_comment1, data=json.dumps({
            "content": "put test",
            "item": self.item2.id
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.url_comment1)
        self.assertEqual(r.data["content"], "put test")
        self.assertEqual(r.datat["item"], self.item2.id)

    def test_patch_comment(self):
        self.post_comment(self.item1.id)

        r = self.client.patch(self.url_comment1, data=json.dumps({
            "content": "patch test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.url_comment1)
        self.assertEqual(r.data["content"], "patch test")

    def test_delete_comment(self):
        self.post_comment(self.item1.id)

        r = self.client.delete(self.url_comment1)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.client.get(self.url_comments)
        self.assertEqual(len(r.data), 0)
