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

    def post_item(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)
        Category.objects.create(name="Test")
        self.assertEqual(Category.objects.count(), 1)
        return self.c.post("/api/items/create", data=json.dumps({
            "name": "name",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "owner": UserProfile.objects.get(id=1),
            "category": Category.objects.get(id=1)
        }), content_type="application/json")

    def post_item_should_not_work_if_price_min_is_bigger_than_price_max(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)
        Category.objects.create(name="Test")
        self.assertEqual(Category.objects.count(), 1)
        return self.c.post("/api/items/create", data=json.dumps({
            "name": "name",
            "description": "test",
            "price_min": 2,
            "price_max": 1,
            "owner": UserProfile.objects.get(id=1),
            "category": Category.objects.get(id=1)
        }), content_type="application/json")

    def archive_item(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)
        Category.objects.create(name="Test")
        self.assertEqual(Category.objects.count(), 1)
        self.c.post("/api/items/create", data=json.dumps({
            "name": "name",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "owner": UserProfile.objects.get(id=1),
            "category": Category.objects.get(id=1)
        }), content_type="application/json")
        return self.c.patch("/api/items/1/archive", data=json.dumps({}), content_type="application/json")

    def unarchive_item(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)
        Category.objects.create(name="Test")
        self.assertEqual(Category.objects.count(), 1)
        self.c.post("/api/items/create", data=json.dumps({
            "name": "name",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "owner": UserProfile.objects.get(id=1),
            "category": Category.objects.get(id=1)
        }), content_type="application/json")
        return self.c.patch("/api/items/1/unarchive", data=json.dumps({}), content_type="application/json")