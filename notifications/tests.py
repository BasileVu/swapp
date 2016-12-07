import json

from django.contrib.auth.models import User
from django.test import TestCase

from items.models import Category, Item
from notifications.models import Notification, OfferNotification


class NotificationAPITest(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        self.other_user = User.objects.create_user(username="user1", email="test@test.com", password="password")

        c1 = Category.objects.create(name="Test1")
        c2 = Category.objects.create(name="Test2")

        Item.objects.create(name="Shoes", description="My old shoes", price_min=10, price_max=30,
                            owner=self.current_user, category=c1)
        Item.objects.create(name="Shirt", description="My old shirt", price_min=5, price_max=30,
                            owner=self.current_user, category=c1)
        Item.objects.create(name="Phone", description="My old phone", price_min=20, price_max=50,
                            owner=self.current_user, category=c2)
        Item.objects.create(name="Car", description="My new car", price_min=35, price_max=50,
                            owner=self.current_user, category=c2)
        Item.objects.create(name="Shoes", description="My old shoes", price_min=10, price_max=30,
                            owner=self.other_user, category=c1)
        Item.objects.create(name="Shirt", description="My old shirt", price_min=5, price_max=30,
                            owner=self.other_user, category=c1)
        Item.objects.create(name="Phone", description="My old phone", price_min=20, price_max=50,
                            owner=self.other_user, category=c2)
        Item.objects.create(name="Car", description="My new car", price_min=35, price_max=50,
                            owner=self.other_user, category=c2)

    def post_offer(self, item_given, item_received, accepted=False, status=0, comment="test"):
        return self.client.post("/api/offers/", data=json.dumps({
            "accepted": accepted,
            "status": status,
            "comment": comment,
            "item_given": item_given,
            "item_received": item_received
        }), content_type="application/json")

    def test_new_offer_creation_notification(self):
        self.client.login(username="username", password="password")

        self.post_offer(1, 8)
        self.post_offer(2, 6)
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)

        self.client.logout()
        self.client.login(username="user1", password="password")

        self.post_offer(5, 3)
        self.post_offer(7, 1)
        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=3).user.username, "username")
        self.assertEqual(OfferNotification.objects.get(pk=3).offer.id, 3)
        self.assertEqual(OfferNotification.objects.get(pk=4).offer.id, 4)
