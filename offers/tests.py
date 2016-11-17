import json

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from items.models import Category, Item


class OfferAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")

        self.other_user = User.objects.create_user(username="user1", email="test@test.com",
                                                   password="password").userprofile

        self.create_item(c1, self.other_user, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.create_item(c2, self.current_user.userprofile, name="Shirt", description="My old shirt", price_min=5,
                         price_max=30)

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def login(self):
        return self.client.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

    def post_offer(self, item_given, item_received, accepted=False, status=0, comment="Test"):
        return self.client.post("/api/offers/", data=json.dumps({
            "accepted": accepted,
            "status": status,
            "comment":  comment,
            "item_given": item_given,
            "item_received": item_received
        }), content_type="application/json")

    def get_offers(self):
        return self.client.get("/api/offers/", content_type="application/json")

    def get_offer(self, id_offer=1):
        return self.client.get("/api/offers/" + str(id_offer) + "/", content_type="application/json")

    def put_offer(self, id_offer, item_given, item_received, accepted=False, status=0, comment="Test"):
        return self.client.put("/api/offers/" + str(id_offer) + "/", data=json.dumps({
            "accepted": accepted,
            "status": status,
            "comment":  comment,
            "item_given": item_given,
            "item_received": item_received
        }), content_type="application/json")

    def delete_offer(self, id_offer=1):
        return self.client.delete("/api/offers/" + str(id_offer) + "/", content_type="application/json")

    def patch_offer(self, id_offer=1, data=json.dumps({"accepted": False})):
        return self.client.patch("/api/offers/" + str(id_offer) + "/", data=data, content_type="application/json")

    def test_post_offer(self):
        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)

    def test_post_offer_on_self_item(self):
        self.login()
        r = self.post_offer(1, 1)
        self.assertEqual(r.status_code, 400)

    def test_post_offer_on_object_not_owned(self):
        self.login()
        r = self.post_offer(1, 2)
        self.assertEqual(r.status_code, 400)

    def test_get_offers(self):
        r = self.get_offers()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)

        r = self.get_offers()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_get_offer(self):
        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)

        r = self.get_offer(id_offer=r.data['id'])
        self.assertEqual(r.status_code, 200)
        r = self.get_offer(id_offer=10)
        self.assertEqual(r.status_code, 404)

    def test_put_offer(self):
        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)
        id_offer = r.data['id']
        r = self.put_offer(1, item_given=2, item_received=1, accepted=True, status=1, comment="Test2")
        self.assertEqual(r.status_code, 200)
        r = self.get_offer(id_offer=id_offer)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['item_given'], 2)
        self.assertEqual(r.data['item_received'], 1)
        self.assertEqual(r.data['accepted'], True)
        self.assertEqual(r.data['status'], 1)
        self.assertEqual(r.data['comment'], "Test2")
        r = self.put_offer(10, 2, 1)
        self.assertEqual(r.status_code, 404)

    def test_patch_offer(self):
        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)
        id_offer = r.data['id']
        r = self.patch_offer(id_offer=id_offer, data=json.dumps({"item_given": 2}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_offer(id_offer=id_offer, data=json.dumps({"item_received": 1}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_offer(id_offer=id_offer, data=json.dumps({"accepted": True}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_offer(id_offer=id_offer, data=json.dumps({"status": 1}))
        self.assertEqual(r.status_code, 200)
        r = self.patch_offer(id_offer=id_offer, data=json.dumps({"comment": "Test2"}))
        self.assertEqual(r.status_code, 200)
        r = self.get_offer(id_offer=id_offer)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['item_given'], 2)
        self.assertEqual(r.data['item_received'], 1)
        self.assertEqual(r.data['accepted'], True)
        self.assertEqual(r.data['status'], 1)
        self.assertEqual(r.data['comment'], "Test2")
        r = self.patch_offer(id_offer=10)
        self.assertEqual(r.status_code, 404)

    def test_delete_offer(self):
        self.login()
        r = self.post_offer(2, 1)
        self.assertEqual(r.status_code, 201)
        id_offer = r.data['id']
        r = self.get_offers()
        self.assertEqual(len(r.data), 1)
        r = self.delete_offer(id_offer=id_offer)
        self.assertEqual(r.status_code, 204)
        r = self.get_offers()
        self.assertEqual(len(r.data), 0)
        r = self.delete_offer(id_offer=10)
        self.assertEqual(r.status_code, 404)