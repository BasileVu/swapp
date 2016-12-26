import json

from django.contrib.auth.models import User
from django.test import TestCase

from items.models import Category, Item
from notifications.models import Notification, OfferNotification, NewOfferNotification, AcceptedOfferNotification, \
    RefusedOfferNotification, CommentNotification, MessageNotification, NoteNotification


class NotificationAPITest(TestCase):
    url_offers = "/api/offers/"
    url_comments = "/api/comments/"
    url_messages = "/api/messages/"
    url_notes = "/api/notes/"

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

    def post_offer(self, id_item_given, id_item_received, accepted=False, status=0, comment="test"):
        return self.client.post(self.url_offers, data=json.dumps({
            "accepted": accepted,
            "status": status,
            "comment": comment,
            "item_given": id_item_given,
            "item_received": id_item_received
        }), content_type="application/json")

    def patch_offer(self, id_offer, accepted):
        return self.client.patch(self.url_offers + str(id_offer) + "/", data=json.dumps({
            "accepted": accepted
        }), content_type="application/json")

    def post_comment(self, id_user, id_item, content="comment test"):
        return self.client.post(self.url_comments, data=json.dumps({
            "content": content,
            "user": id_user,
            "item": id_item
        }), content_type="application/json")

    def post_note(self, id_user, id_offer, text="note test", note=0):
        return self.client.post(self.url_notes, data=json.dumps({
            "user": id_user,
            "offer": id_offer,
            "text": text,
            "note": note
        }), content_type="application/json")

    def post_message(self, id_user_from, id_user_to, message="message test"):
        return self.client.post(self.url_messages, data=json.dumps({
            "text": message,
            "user_from": id_user_from,
            "user_to": id_user_to
        }), content_type="application/json")

    def test_new_offer_creation_notification(self):
        self.client.login(username="username", password="password")

        self.post_offer(1, 7)
        self.post_offer(2, 6)
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(OfferNotification.objects.count(), 2)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(NewOfferNotification.objects.count(), 2)

        self.client.logout()
        self.client.login(username="user1", password="password")

        self.post_offer(5, 3)
        self.post_offer(7, 1)
        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=3).user.username, "username")
        self.assertEqual(OfferNotification.objects.count(), 4)
        self.assertEqual(OfferNotification.objects.get(pk=3).offer.id, 3)
        self.assertEqual(OfferNotification.objects.get(pk=4).offer.id, 4)
        self.assertEqual(NewOfferNotification.objects.count(), 4)

    def test_offer_accepted_notification(self):
        self.client.login(username="username", password="password")

        self.post_offer(1, 7)
        self.post_offer(2, 6)

        r = self.patch_offer(1, True)
        self.assertEqual(r.status_code, 200)

        self.patch_offer(2, True)
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(OfferNotification.objects.count(), 4)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(AcceptedOfferNotification.objects.count(), 2)

    def test_offer_refused_notification(self):
        self.client.login(username="username", password="password")

        self.post_offer(1, 7)
        self.post_offer(2, 6)

        r = self.patch_offer(1, False)
        self.assertEqual(r.status_code, 200)

        self.patch_offer(2, False)
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(OfferNotification.objects.count(), 4)
        self.assertEqual(OfferNotification.objects.get(pk=1).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=2).offer.id, 2)
        self.assertEqual(OfferNotification.objects.get(pk=3).offer.id, 1)
        self.assertEqual(OfferNotification.objects.get(pk=4).offer.id, 2)
        self.assertEqual(RefusedOfferNotification.objects.count(), 2)

    def test_new_comment_notification(self):
        self.client.login(username="username", password="password")

        self.post_comment(1, 5)
        self.post_comment(1, 6)
        self.post_comment(1, 7)
        self.post_comment(1, 8)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(CommentNotification.objects.count(), 4)

    def test_new_note_notification(self):
        self.client.login(username="username", password="password")

        self.post_offer(1, 7)
        self.post_offer(2, 6)

        self.patch_offer(1, True)
        self.patch_offer(2, True)

        self.post_note(1, 1)
        self.post_note(1, 2)

        self.assertEqual(Notification.objects.count(), 6)
        self.assertEqual(Notification.objects.get(pk=5).user.username, "user1")
        self.assertEqual(NoteNotification.objects.count(), 2)

    def test_new_message_notification(self):
        self.client.login(username="username", password="password")

        self.post_message(1, 2)
        self.post_message(1, 2)
        self.post_message(2, 1)
        self.post_message(2, 1)

        self.assertEqual(Notification.objects.count(), 4)
        self.assertEqual(Notification.objects.get(pk=1).user.username, "user1")
        self.assertEqual(MessageNotification.objects.count(), 4)
