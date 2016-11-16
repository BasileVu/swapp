import json

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from items.models import Category


class OfferAPITests(TestCase):
    c = Client()

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()
        Category.objects.create(name="Test")
        Category.objects.create(name="Test2")
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

    def post_offer(self, name="name", description="description", price_min=1, price_max=2, category=1, image_set=list()):
        return self.c.post("/api/items/", data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "image_set": image_set
        }), content_type="application/json")

    def get_offer(self):
        return self.c.get("/api/items/", content_type="application/json")

    def get_offer(self, id_item=1):
        return self.c.get("/api/items/" + str(id_item) + "/", content_type="application/json")

    def put_offer(self, id_item=1, name="name", description="description", price_min=1, price_max=2, category=1, image_set=list()):
        return self.c.put("/api/items/" + str(id_item) + "/", data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "image_set": image_set
        }), content_type="application/json")

    def delete_offer(self, id_item=1):
        return self.c.delete("/api/items/" + str(id_item) + "/", content_type="application/json")

    def patch_offer(self, id_item=1, data=json.dumps({"name": "test"})):
        return self.c.patch("/api/items/" + str(id_item) + "/", data=data, content_type="application/json")

    def test_post_offer(self):
        self.c.login()
        r = self.post_item()
        self.assertEqual(r.status_code, 201)

    def test_get_offers(self):
        r = self.get_items()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)
        self.client.login()
        r = self.post_item()
        self.assertEqual(r.status_code, 201)
        r = self.get_items()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_get_offer(self):
        self.client.login()
        r = self.post_item()
        self.assertEqual(r.status_code, 201)
        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, 200)
        r = self.get_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_put_offer(self):
        self.client.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        id_item = r.data['id']
        r = self.put_item(id_item=id_item, name="test2", description="test2", price_min=2, price_max=3, category=2)
        self.assertEqual(r.status_code, 200)
        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category'], 2)
        r = self.put_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_patch_offer(self):
        self.client.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        id_item = r.data['id']
        r = self.patch_item(id_item=id_item, data=json.dumps({"name": "test2"}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_item(id_item=id_item, data=json.dumps({"description": "test2"}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_item(id_item=id_item, data=json.dumps({"price_min": 2}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_item(id_item=id_item, data=json.dumps({"price_max": 3}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_item(id_item=id_item, data=json.dumps({"category": 2}))
        self.assertEqual(r.status_code, 200)
        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category'], 2)
        r = self.patch_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_delete_offer(self):
        self.client.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        id_item = r.data['id']
        r = self.get_items()
        self.assertEqual(len(r.data), 1)
        r = self.delete_item(id_item=id_item)
        self.assertEqual(r.status_code, 204)
        r = self.get_items()
        self.assertEqual(len(r.data), 0)
        r = self.delete_item(id_item=10)
        self.assertEqual(r.status_code, 404)