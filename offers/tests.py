import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from items.models import Category, Item
from offers.models import Offer


class OfferAPITests(TestCase):
    offers_url = "/api/offers/"

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def post_offer(self, id_item_given, id_item_received, accepted=False, comment="Test"):
        return self.client.post(self.offers_url, data=json.dumps({
            "accepted": accepted,
            "comment":  comment,
            "item_given": id_item_given,
            "item_received": id_item_received
        }), content_type="application/json")

    def get_offer(self, id_offer=1):
        return self.client.get("%s%d/" % (self.offers_url, id_offer), content_type="application/json")

    def put_offer(self, id_offer, accepted=False, comment="Test"):
        return self.client.put("%s%d/" % (self.offers_url, id_offer), data=json.dumps({
            "accepted": accepted,
            "comment":  comment,
        }), content_type="application/json")

    def patch_offer(self, id_offer=1, **kwargs):
        return self.client.patch("%s%d/" % (self.offers_url, id_offer), data=json.dumps(kwargs),
                                 content_type="application/json")

    def delete_offer(self, id_offer=1):
        return self.client.delete("%s%d/" % (self.offers_url, id_offer), content_type="application/json")

    def login1(self):
        self.client.logout()
        self.client.login(username="user1", password="password")

    def login2(self):
        self.client.logout()
        self.client.login(username="user2", password="password")

    def setUp(self):
        self.current_user = User.objects.create_user(username="user1", email="test@test.com", password="password")
        self.other_user = User.objects.create_user(username="user2", email="test@test.com", password="password")

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")

        self.item1 = self.create_item(c1, self.current_user, name="Pencil", description="Not used", price_min=1,
                                      price_max=2)
        self.item2 = self.create_item(c1, self.current_user, name="Shoes", description="My old shoes", price_min=10,
                                      price_max=30)
        self.item3 = self.create_item(c2, self.other_user, name="Shirt", description="My old shirt", price_min=5,
                                      price_max=30)

        self.login1()

    def test_post_offer(self):
        r = self.post_offer(self.item2.id, self.item3.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_post_offer_on_self_item(self):
        r = self.post_offer(self.item2.id, self.item2.id)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_on_object_not_owned(self):
        r = self.post_offer(self.item3.id, self.item2.id)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_on_invalid_price_range(self):
        r = self.post_offer(self.item1.id, self.item3.id)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Offer.objects.count(), 0)

    def test_cannot_create_already_created_offer(self):
        r = self.post_offer(self.item2.id, self.item3.id)
        r = self.post_offer(self.item2.id, self.item3.id)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_offer(self):
        r = self.post_offer(self.item2.id, self.item3.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_offer()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["accepted"], False)
        self.assertEqual(r.data["answered"], False)
        self.assertEqual(r.data["comment"], "Test")
        self.assertEqual(r.data["item_given"], self.item2.id)
        self.assertEqual(r.data["item_received"], self.item3.id)

    def test_get_offer_not_existing(self):
        r = self.get_offer(id_offer=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_offer(self):
        self.post_offer(self.item2.id, self.item3.id)

        self.login2()
        r = self.put_offer(1, accepted=True, comment="Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_offer()
        self.assertEqual(r.data["accepted"], True)
        self.assertEqual(r.data["answered"], True)
        self.assertEqual(r.data["comment"], "Test2")

    def test_put_offer_not_found(self):
        r = self.put_offer(10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer(self):
        self.post_offer(self.item2.id, self.item3.id)

        r = self.patch_offer(comment="Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        self.login2()
        r = self.patch_offer(accepted=True)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_offer()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["item_given"], self.item2.id)
        self.assertEqual(r.data["item_received"], self.item3.id)
        self.assertEqual(r.data["accepted"], True)
        self.assertEqual(r.data["answered"], True)
        self.assertEqual(r.data["comment"], "Test2")

    def test_patch_offer_not_existing(self):
        r = self.patch_offer(id_offer=1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_accept_or_refuse_own_offer(self):
        r = self.post_offer(self.item2.id, self.item3.id)
        r = self.patch_offer(id_offer=r.data["id"], accepted=True)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_offer(self):
        r = self.post_offer(self.item2.id, self.item3.id)
        self.post_offer(self.item1.id, self.item3.id)

        id_offer = r.data["id"]
        r = self.delete_offer(id_offer=id_offer)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_accepted_offer(self):
        o = Offer.objects.create(item_given=self.item2, item_received=self.item3, accepted=True, answered=True)
        r = self.delete_offer(id_offer=o.id)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_not_found(self):
        r = self.delete_offer(id_offer=1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
