import json

from django.test import Client
from django.test import TestCase
from items.models import *
from users.models import *


class ItemTests(TestCase):
    def test_item_creation(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)
        Category.objects.create(name="Test")
        self.assertEqual(Category.objects.count(), 1)
        Item.objects.create(name="Test", description="Test", price_min=1, price_max=2, archived=0,
                            category=Category.objects.get(id=1),
                            owner=UserProfile.objects.get(id=1))
        self.assertEqual(Item.objects.count(), 1)


class ItemAPITests(TestCase):
    c = Client()

    def setUp(self):
        User.objects.create_user(username="username", email="test@test.com", password="password")
        Category.objects.create(name="Test")
        self.login()

    def login(self):
        return self.c.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

    def test_post_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 201)

    def test_post_item_should_return_400_if_price_min_is_bigger_than_price_max(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 2,
            "price_max": 1,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_post_item_should_return_400_if_json_data_is_invalid(self):
        r = self.c.post("/api/items/", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_archive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 201)
        r = self.c.patch("/api/items/1/archive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 200)

    def test_unarchive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 201)
        r = self.c.patch("/api/items/1/unarchive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 200)
