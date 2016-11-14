import json

import logging
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
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()
        Category.objects.create(name="Test")
        self.login()

    def post_user(self, username="username", email="test@test.com", password="password"):
        return self.c.post("/api/users/", data=json.dumps({
            "username": username,
            "email": email,
            "password": password
        }), content_type="application/json")

    def login(self):
        return self.c.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

    def post_item(self):
        return self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1,
        }), content_type="application/json")

    def test_post_item(self):
        r = self.post_item()
        print(r.content)
        print(r)
        print(r.status_code)
        logging.getLogger('my_logger').error(r.status_code)
        logging.getLogger('my_logger').error(r)
        logging.getLogger('my_logger').error(r.content)
        self.assertEqual(r.status_code, 201)

    def test_post_item_price_min_bigger_than_price_max(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 2,
            "price_max": 1,
            "category": 1,
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_post_item_json_data_invalid(self):
        r = self.c.post("/api/items/", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_post_item_user_location_not_specified(self):
        self.current_user.userprofile.location = ""
        self.current_user.userprofile.save()
        r = self.post_item()
        self.assertEqual(r.status_code, 400)
    '''
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
    '''
