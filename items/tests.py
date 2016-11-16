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

    def post_item(self, name="name", description="description", price_min=1, price_max=2, category=1, image_set=list()):
        return self.c.post("/api/items/", data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "image_set": image_set
        }), content_type="application/json")

    def test_post_item(self):
        r = self.post_item()
        self.assertEqual(r.status_code, 201)

    def test_post_item_price_min_bigger_than_price_max(self):
        r = self.post_item(price_min=2, price_max=1)
        self.assertEqual(r.status_code, 400)

    def test_post_item_json_data_invalid(self):
        r = self.c.post("/api/items/", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    '''
    def test_post_item_user_location_not_specified(self):
        self.current_user.userprofile.location = ""
        self.current_user.userprofile.save()
        r = self.post_item()
        self.assertEqual(r.status_code, 400)
    '''
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


class ItemSearchApiTests(TestCase):

    url = "/api/items/"

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def setUp(self):
        u1 = User.objects.create_user(username="user1", email="test@test.com", password="password").userprofile
        u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password").userprofile

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")
        c3 = Category.objects.create(name="Test3")

        self.create_item(c1, u1, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.create_item(c2, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30)
        self.create_item(c3, u1, name="Ring", description="My precious", price_min=100, price_max=500)
        self.create_item(c1, u2, name="New mouse", description="Brand new", price_min=20, price_max=100)
        self.create_item(c2, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000)

        self.client.login()

    def test_list_item_no_filter(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

    def test_list_item_category(self):
        r = self.client.get(self.url + "?category=category")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?category=test")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?category=Test")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?category=Test2")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?category=Test3")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)


    def test_list_item_q(self):
        r = self.client.get(self.url + "?q=my")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 3)

        r = self.client.get(self.url + "?q=shoes")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?q=sh")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

    def test_list_item_price_min(self):
        r = self.client.get(self.url + "?price_min=0")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_min=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_min=10")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 4)

        r = self.client.get(self.url + "?price_min=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

    def test_list_item_price_max(self):
        r = self.client.get(self.url + "?price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?price_max=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_max=10000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

    def test_list_item_price_range(self):
        r = self.client.get(self.url + "?price_min=0&price_max=0")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=0&price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=5&price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=5&price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?price_min=10&price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=500&price_max=10000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=0&price_max=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)
