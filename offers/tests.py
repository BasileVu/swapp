import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from items.models import Category, Item
from offers.models import Offer


class OfferAPITests(TestCase):
    offers_url = "/api/offers/"

    def post_offer(self, item_given, item_received, accepted=False, comment="Test"):
        return self.client.post(self.offers_url, data=json.dumps({
            "accepted": accepted,
            "comment":  comment,
            "item_given": item_given.id,
            "item_received": item_received.id
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

        self.c1 = Category.objects.create(name="Test")
        self.c2 = Category.objects.create(name="Test2")

        self.item1 = Item.objects.create(owner=self.current_user, category=self.c1, price_min=10, price_max=30)
        self.item2 = Item.objects.create(owner=self.other_user, category=self.c2, price_min=5, price_max=30)

        self.login1()

    def test_post_offer(self):
        r = self.post_offer(self.item1, self.item2)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_post_offer_on_self_item(self):
        r = self.post_offer(self.item1, self.item1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_on_object_not_owned(self):
        r = self.post_offer(self.item2, self.item1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_on_invalid_price_range(self):
        i1 = Item.objects.create(owner=self.current_user, category=self.c1, price_min=1, price_max=2)
        r = self.post_offer(i1, self.item2)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Offer.objects.count(), 0)

    def test_cannot_create_already_created_offer(self):
        self.post_offer(self.item1, self.item2)
        r = self.post_offer(self.item1, self.item2)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_offer_if_already_offer_created_with_wanted_item_for_this_item(self):
        self.post_offer(self.item1, self.item2)

        self.login2()
        r = self.post_offer(self.item2, self.item1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_offer_for_traded_item(self):
        self.item2.traded = True
        self.item2.save()

        r = self.post_offer(self.item1, self.item2)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_offer_for_archived_item(self):
        self.item2.archived = True
        self.item2.save()

        r = self.post_offer(self.item1, self.item2)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_offer(self):
        r = self.post_offer(self.item1, self.item2)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_offer()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["accepted"], False)
        self.assertEqual(r.data["answered"], False)
        self.assertEqual(r.data["comment"], "Test")
        self.assertEqual(r.data["item_given"], self.item1.id)
        self.assertEqual(r.data["item_received"], self.item2.id)

    def test_get_offer_not_existing(self):
        r = self.get_offer(id_offer=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_offer(self):
        self.post_offer(self.item1, self.item2)

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
        self.post_offer(self.item1, self.item2)

        r = self.patch_offer(comment="Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["comment"], "Test2")

    def test_patch_offer_not_existing(self):
        r = self.patch_offer()
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_answered_changed_when_offer_accepted(self):
        self.post_offer(self.item1, self.item2)

        self.login2()
        r = self.patch_offer(accepted=True)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_offer()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["item_given"], self.item1.id)
        self.assertEqual(r.data["item_received"], self.item2.id)
        self.assertEqual(r.data["accepted"], True)
        self.assertEqual(r.data["answered"], True)
        self.assertEqual(r.data["comment"], "Test")

    def test_items_traded_when_offer_accepted(self):
        self.post_offer(self.item1, self.item2)
        self.login2()

        self.patch_offer(accepted=True)
        self.assertEqual(Item.objects.get(pk=self.item1.id).traded, True)
        self.assertEqual(Item.objects.get(pk=self.item2.id).traded, True)

    def test_other_offers_refused_and_deleted_when_offer_accepted(self):
        i3 = Item.objects.create(owner=self.current_user, category=self.c1, price_min=10, price_max=30)
        i4 = Item.objects.create(owner=self.other_user, category=self.c1, price_min=10, price_max=30)
        i5 = Item.objects.create(owner=self.current_user, category=self.c1, price_min=10, price_max=30)

        o1 = Offer.objects.create(item_given=self.item1, item_received=self.item2)
        o2 = Offer.objects.create(item_given=self.item1, item_received=i4)
        o3 = Offer.objects.create(item_given=self.item2, item_received=i3)
        o4 = Offer.objects.create(item_given=i3, item_received=i4)
        o5 = Offer.objects.create(item_given=i5, item_received=self.item2)
        o6 = Offer.objects.create(item_given=i5, item_received=i4)

        self.login2()

        self.patch_offer(o1.id, accepted=True)

        self.assertEqual(Offer.objects.filter(pk=o2.id).count(), 0)
        self.assertEqual(Offer.objects.filter(pk=o3.id).count(), 0)
        self.assertEqual(Offer.objects.get(pk=o4.id).answered, False)
        self.assertEqual(Offer.objects.get(pk=o5.id).answered, True)
        self.assertEqual(Offer.objects.get(pk=o5.id).accepted, False)
        self.assertEqual(Offer.objects.get(pk=o6.id).answered, False)

    def test_cannot_change_answered_status(self):
        self.post_offer(self.item1, self.item2)
        self.patch_offer(answered=True)

        self.login2()
        self.patch_offer(answered=True)

        r = self.get_offer()
        self.assertEqual(r.data["answered"], False)

    def test_cannot_accept_or_refuse_own_offer(self):
        self.post_offer(self.item1, self.item2)
        r = self.patch_offer(accepted=True)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_change_accepted_status_after_accepted(self):
        self.post_offer(self.item1, self.item2)

        self.login2()
        self.patch_offer(accepted=True)
        r = self.patch_offer(accepted=False)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_edit_accepted_offer(self):
        self.post_offer(self.item1, self.item2)

        self.login2()
        self.patch_offer(accepted=True)

        r = self.patch_offer(comment="Test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.login1()
        r = self.patch_offer(comment="Test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_offer(self):
        self.post_offer(self.item1, self.item2)
        r = self.delete_offer()
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_offer_of_another_user(self):
        self.post_offer(self.item1, self.item2)

        self.login2()
        r = self.delete_offer()
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_delete_accepted_offer(self):
        o = Offer.objects.create(item_given=self.item1, item_received=self.item2, accepted=True, answered=True)
        r = self.delete_offer(id_offer=o.id)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_not_found(self):
        r = self.delete_offer(id_offer=1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
