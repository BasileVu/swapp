import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from items.models import Category, Item
from notifications.models import Notification, OfferNotification, NewOfferNotification, AcceptedOfferNotification, \
    RefusedOfferNotification, CommentNotification, MessageNotification, NoteNotification


class NotificationAPITest(TestCase):
    offers_url = "/api/offers/"
    comments_url = "/api/comments/"
    messages_url = "/api/messages/"
    notes_url = "/api/notes/"
    notifications_url = "/api/notifications/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="user1", email="test@test.com", password="password")
        self.other_user = User.objects.create_user(username="user2", email="test@test.com", password="password")

        c1 = Category.objects.create(name="Test1")
        c2 = Category.objects.create(name="Test2")

        self.item1 = Item.objects.create(name="Shoes", description="My old shoes", price_min=10, price_max=30,
                                         owner=self.current_user, category=c1)
        self.item2 = Item.objects.create(name="Shirt", description="My old shirt", price_min=5, price_max=30,
                                         owner=self.current_user, category=c1)
        self.item3 = Item.objects.create(name="Phone", description="My old phone", price_min=20, price_max=50,
                                         owner=self.current_user, category=c2)
        self.item4 = Item.objects.create(name="Car", description="My new car", price_min=35, price_max=50,
                                         owner=self.current_user, category=c2)
        self.item5 = Item.objects.create(name="Shoes", description="My old shoes", price_min=10, price_max=30,
                                         owner=self.other_user, category=c1)
        self.item6 = Item.objects.create(name="Shirt", description="My old shirt", price_min=5, price_max=30,
                                         owner=self.other_user, category=c1)
        self.item7 = Item.objects.create(name="Phone", description="My old phone", price_min=20, price_max=50,
                                         owner=self.other_user, category=c2)
        self.item8 = Item.objects.create(name="Car", description="My new car", price_min=35, price_max=50,
                                         owner=self.other_user, category=c2)

    def post_offer(self, item_given, item_received, comment="test"):
        return self.client.post(self.offers_url, data=json.dumps({
            "comment": comment,
            "item_given": item_given.id,
            "item_received": item_received.id
        }), content_type="application/json")

    def patch_offer(self, id_offer, **kwargs):
        return self.client.patch("%s%d/" % (self.offers_url, id_offer), data=json.dumps(kwargs),
                                 content_type="application/json")

    def post_comment(self, user, item, content="comment test"):
        return self.client.post(self.comments_url, data=json.dumps({
            "content": content,
            "user": user.id,
            "item": item.id
        }), content_type="application/json")

    def post_note(self, user, id_offer, text="note test", note=0):
        return self.client.post(self.notes_url, data=json.dumps({
            "user": user.id,
            "offer": id_offer,
            "text": text,
            "note": note
        }), content_type="application/json")

    def post_message(self, user_from, user_to, message="message test"):
        return self.client.post(self.messages_url, data=json.dumps({
            "text": message,
            "user_from": user_from.id,
            "user_to": user_to.id
        }), content_type="application/json")

    def patch_notification(self, id_notification, read):
        return self.client.patch("%s%d/" % (self.notifications_url, id_notification), data=json.dumps({
            "read": read
        }), content_type="application/json")

    def get_notifications(self):
        return self.client.get(self.notifications_url)

    def login1(self):
        self.client.logout()
        self.client.login(username="user1", password="password")

    def login2(self):
        self.client.logout()
        self.client.login(username="user2", password="password")

    def test_get_notifications(self):
        self.login1()

        r = self.get_notifications()
        self.assertEqual(len(r.data), 0)

        self.post_offer(self.item1, self.item7)

        self.login2()
        r = self.get_notifications()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertIn("id", r.data[0])
        self.assertIn("content", r.data[0])
        self.assertIn("read", r.data[0])
        self.assertIn("date", r.data[0])

    def test_get_notification_order_by_date(self):
        now = timezone.now()

        Notification.objects.create(content="test1", date=now + timezone.timedelta(seconds=4),
                                    user=self.current_user)
        Notification.objects.create(content="test2", date=now + timezone.timedelta(seconds=2),
                                    user=self.current_user)
        Notification.objects.create(content="test3", date=now + timezone.timedelta(seconds=3),
                                    user=self.current_user)

        self.login1()

        r = self.get_notifications()
        self.assertEquals(r.data[0]["content"], "test1")
        self.assertEquals(r.data[1]["content"], "test3")
        self.assertEquals(r.data[2]["content"], "test2")

    def test_patch_notification(self):
        self.login1()

        n = Notification.objects.create(content="test1", user=self.current_user)
        r = self.patch_notification(n.id, True)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.get(pk=n.id).read, True)

    def test_new_offer_creation_notification(self):
        self.login1()
        self.post_offer(self.item1, self.item7)
        self.post_offer(self.item2, self.item6)

        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user2")
        self.assertEqual(OfferNotification.objects.count(), 2)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(NewOfferNotification.objects.count(), 2)

        self.login2()
        self.post_offer(self.item5, self.item3)

        self.assertEqual(Notification.objects.count(), 3)
        self.assertEqual(Notification.objects.get(pk=3).user.username, "user1")
        self.assertEqual(OfferNotification.objects.count(), 3)
        self.assertEqual(OfferNotification.objects.get(pk=3).offer.id, 3)
        self.assertEqual(NewOfferNotification.objects.count(), 3)

    def test_offer_accepted_notification(self):
        self.login1()
        self.post_offer(self.item1, self.item7)
        self.post_offer(self.item2, self.item6)

        self.login2()
        self.patch_offer(1, accepted=True)
        self.patch_offer(2, accepted=True)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user2")
        self.assertEqual(OfferNotification.objects.count(), 4)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(AcceptedOfferNotification.objects.count(), 2)

    def test_offer_refused_notification(self):
        self.login1()
        self.post_offer(self.item1, self.item7)
        self.post_offer(self.item2, self.item6)

        self.login2()
        self.patch_offer(1, accepted=False)
        self.patch_offer(2, accepted=False)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user2")
        self.assertEqual(OfferNotification.objects.count(), 4)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(OfferNotification.objects.get(pk=3).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=4).offer.id, 2)
        self.assertEqual(RefusedOfferNotification.objects.count(), 2)

    def test_new_comment_notification(self):
        self.login1()

        self.post_comment(self.current_user, self.item5)
        self.post_comment(self.current_user, self.item6)
        self.post_comment(self.current_user, self.item7)
        self.post_comment(self.current_user, self.item8)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user2")
        self.assertEqual(CommentNotification.objects.count(), 4)

    def test_new_note_notification(self):
        self.login1()
        self.post_offer(self.item1, self.item7)
        self.post_offer(self.item2, self.item6)

        self.login2()
        self.patch_offer(1, accepted=True)
        self.patch_offer(2, accepted=True)
        self.post_note(self.current_user, 1)
        self.post_note(self.current_user, 2)

        self.assertEqual(Notification.objects.count(), 6)
        self.assertEqual(Notification.objects.get(pk=5).user.username, "user2")
        self.assertEqual(NoteNotification.objects.count(), 2)

    def test_new_message_notification(self):
        self.login1()

        self.post_message(self.current_user, self.other_user)
        self.post_message(self.current_user, self.other_user)
        self.post_message(self.other_user, self.current_user)
        self.post_message(self.other_user, self.current_user)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user2")
        self.assertEqual(MessageNotification.objects.count(), 4)
