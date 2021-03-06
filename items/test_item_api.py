import json

from django.test import TestCase
from rest_framework import status

from comments.models import *
from items.models import *
from swapp import settings
from users.models import *


class ItemBaseTest(TestCase):
    url = "/api/items/"

    default_keyinfo_set = [
        {
            "key": "color",
            "info": "crimson"
        },
        {
            "key": "quality",
            "info": "top notch"
        }
    ]
    default_delivery_methods = [1, 2, 3]
    get_default_delivery_methods = [
        {
            "id": 1,
            "name": "At my place"
        },
        {
            "id": 2,
            "name": "At any place"
        },
        {
            "id": 3,
            "name": "By mail"
        }
    ]

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password",
                                                     first_name="first",
                                                     last_name="last")
        self.another_user = User.objects.create_user(username="username2", password="password", first_name="first2",
                                                     last_name="last2")

        self.c1 = Category.objects.create(name="test")
        self.c2 = Category.objects.create(name="test2")

        self.dm1 = DeliveryMethod.objects.create(name="At my place")
        self.dm2 = DeliveryMethod.objects.create(name="At any place")
        self.dm3 = DeliveryMethod.objects.create(name="By mail")

    def build_update_info(self, name="name", description="description", price_min=1, price_max=2, category=1,
                          keyinfo_set=None, delivery_methods=None):
        return {
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "keyinfo_set": keyinfo_set if keyinfo_set is not None else self.default_keyinfo_set,
            "delivery_methods": delivery_methods if delivery_methods is not None else self.default_delivery_methods
        }

    def post_item(self, **kwargs):
        return self.client.post(self.url, data=json.dumps(self.build_update_info(**kwargs)),
                                content_type="application/json")

    def login(self, username="username", password="password"):
        self.client.login(username=username, password=password)

    def login1(self):
        self.client.logout()
        self.client.login(username="username1", password="password")

    def login2(self):
        self.client.logout()
        self.client.login(username="username2", password="password")

    def get_item(self, item_id=1):
        return self.client.get("%s%d/" % (self.url, item_id), content_type="application/json")

    def post_image(self, image_name="test.png"):
        with open("%s/%s" % (settings.MEDIA_TEST, image_name), "rb") as data:
            return self.client.post("/api/account/image/", {"image": data}, format="multipart")


class ItemPostTests(ItemBaseTest):
    def setUp(self):
        super().setUp()
        self.login()

    def test_post_item_not_logged_in(self):
        self.client.logout()
        r = self.post_item()
        self.assertEqual(r.status_code, 401)

    def test_post_item_logged_in(self):
        r = self.post_item()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_post_item_price_min_bigger_than_price_max(self):
        r = self.post_item(price_min=2, price_max=1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Item.objects.count(), 0)

    def test_post_item_json_data_invalid(self):
        r = self.client.post(self.url, data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class ItemGetTests(ItemBaseTest):
    def setUp(self):
        super().setUp()
        self.login()
        self.post_item()
        self.post_image()
        self.client.logout()

    def test_get_item(self):
        # another user likes the item of the user "username" to check number of likes
        self.item = Item.objects.get(pk=1)
        Like.objects.create(user=self.another_user, item=self.item)

        # other items in the same category to check similar
        id1 = Item.objects.create(owner=self.current_user, price_min=1, price_max=2, category=self.c1).id
        id2 = Item.objects.create(owner=self.current_user, price_min=1, price_max=2, category=self.c1).id

        # change owner location to check owner_location
        self.current_user.location.city = "city"
        self.current_user.location.country = "country"
        self.current_user.location.save()

        # change owner coordinates to check owner_coordinates
        self.current_user.coordinates.latitude = 4
        self.current_user.coordinates.longitude = 4
        self.current_user.coordinates.save()

        r = self.get_item()

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["owner_username"], "username")
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["name"], "name")
        self.assertEqual(r.data["description"], "description")
        self.assertEqual(r.data["price_min"], 1)
        self.assertEqual(r.data["price_max"], 2)
        self.assertEqual(r.data["category"]["id"], 1)
        self.assertEqual(r.data["category"]["name"], "test")
        self.assertEqual(r.data["views"], 1)
        self.assertEqual(r.data["comments"], 0)
        self.assertEqual(r.data["liked"], False)
        self.assertEqual(r.data["likes"], 1)
        self.assertEqual(r.data["keyinfo_set"], self.default_keyinfo_set)
        self.assertEqual(r.data["delivery_methods"], self.get_default_delivery_methods)
        self.assertEqual(r.data["similar"][0]["id"], id1)
        self.assertEqual(r.data["similar"][1]["id"], id2)
        self.assertEqual(r.data["owner_location"], "city, country")
        self.assertEqual(r.data["owner_coordinates"], {"latitude": 4, "longitude": 4})
        self.assertNotEqual(r.data["owner_picture_url"], None)
        self.assertIn("images", r.data)
        self.assertEqual(r.data["traded"], False)
        self.assertEqual(r.data["archived"], False)

    def test_get_item_not_existing(self):
        r = self.get_item(item_id=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_should_increment_views(self):
        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["views"], 1)

        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["views"], 2)

    def test_get_item_not_liked_logged_in(self):
        self.login()
        r = self.get_item()
        self.assertEqual(r.data["liked"], False)

    def test_get_item_liked(self):
        self.item = Item.objects.get(pk=1)
        Like.objects.create(user=self.another_user, item=self.item)

        self.login2()
        r = self.get_item()
        self.assertEqual(r.data["liked"], True)


class ItemPatchTests(ItemBaseTest):
    def patch_item(self, item_id=1, **kwargs):
        return self.client.patch("%s%d/" % (self.url, item_id), data=json.dumps(kwargs),
                                 content_type="application/json")

    def setUp(self):
        super().setUp()
        self.login()
        self.item = Item.objects.get(pk=self.post_item().data["id"])

    def test_patch_item_not_logged_in(self):
        self.client.logout()
        r = self.patch_item(name="test2")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_name(self):
        r = self.patch_item(name="test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], "test2")

    def test_patch_description(self):
        r = self.patch_item(description="test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["description"], "test2")

    def test_patch_price_min(self):
        r = self.patch_item(price_min=2)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["price_min"], 2)

    def test_patch_price_max(self):
        r = self.patch_item(price_max=3)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["price_max"], 3)

    def test_patch_category(self):
        r = self.patch_item(category=2)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["category"], 2)

    def test_patch_keyinfo_set_empty(self):
        r = self.patch_item(keyinfo_set=[])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["keyinfo_set"], [])

    def test_patch_keyinfo_set_not_empty(self):
        data = [{"key": "key", "info": "info"}]

        r = self.patch_item(keyinfo_set=data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["keyinfo_set"], data)

    def test_patch_delivery_methods_empty(self):
        r = self.patch_item(delivery_methods=[])
        # At least, one delivery method is required
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.get_item()
        self.assertEquals(r.data["delivery_methods"], self.get_default_delivery_methods)

    def test_patch_delivery_methods_not_empty(self):
        r = self.patch_item(delivery_methods=[2])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["delivery_methods"], [2])

    def test_cannot_set_min_price_greater_than_max_price(self):
        r = self.patch_item(price_min=3)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.get_item()
        self.assertEquals(r.data["price_min"], 1)

    def test_cannot_set_max_price_smaller_than_min_price(self):
        r = self.patch_item(price_max=0)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_edit_item_with_refused_offers(self):
        i2 = Item.objects.create(owner=self.another_user, price_min=1, price_max=2, category=self.c1)
        Offer.objects.create(item_given=i2, item_received=self.item, answered=True, accepted=False)

        r = self.patch_item(self.item.id, description="test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_cannot_edit_item_with_pending_initiated_offers(self):
        i2 = Item.objects.create(owner=self.another_user, price_min=1, price_max=2, category=self.c1)
        Offer.objects.create(item_given=i2, item_received=self.item, answered=False)

        r = self.patch_item(self.item.id, description="test2")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_edit_item_with_pending_offers(self):
        i2 = Item.objects.create(owner=self.another_user, price_min=1, price_max=2, category=self.c1)
        Offer.objects.create(item_given=self.item, item_received=i2, answered=False)

        r = self.patch_item(self.item.id, description="test2")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_edit_item_if_traded(self):
        self.item.traded = True
        self.item.save()

        r = self.patch_item(description="test2")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_edit_item_if_archived(self):
        self.item.archived = True
        self.item.save()

        r = self.patch_item(description="test2")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class ItemPutTests(ItemBaseTest):
    def put_item(self, item_id=1, **kwargs):
        return self.client.put("%s%d/" % (self.url, item_id), data=json.dumps(self.build_update_info(**kwargs)),
                               content_type="application/json")

    def setUp(self):
        super().setUp()
        self.login()
        self.post_item()

    def test_put_item_not_logged_in(self):
        self.client.logout()
        r = self.put_item()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_item(self):
        keyinfo_set = [{"key": "test", "info": "test2"}, {"key": "test3", "info": "test4"}]
        delivery_methods = [1, 3]
        get_delivery_methods = [
            {
                "id": 1,
                "name": "At my place"
            },
            {
                "id": 3,
                "name": "By mail"
            }
        ]
        r = self.put_item(name="test2", description="test2", price_min=2, price_max=3, category=2,
                          keyinfo_set=keyinfo_set, delivery_methods=delivery_methods)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], "test2")
        self.assertEqual(r.data["description"], "test2")
        self.assertEqual(r.data["price_min"], 2)
        self.assertEqual(r.data["price_max"], 3)
        self.assertEqual(r.data["category"]["id"], 2)
        self.assertEqual(r.data["category"]["name"], "test2")
        self.assertEqual(r.data["keyinfo_set"], keyinfo_set)
        self.assertEqual(r.data["delivery_methods"], get_delivery_methods)

    def test_put_item_not_existing(self):
        r = self.put_item(item_id=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class ItemCommentTests(ItemBaseTest):
    def setUp(self):
        super().setUp()
        self.login(username="username2", password="password")
        self.post_image()
        self.client.logout()

        self.item = Item.objects.create(owner=self.current_user, price_min=1, price_max=2, category=self.c1)

    def check_get_comment_data_complete(self, data, comment):
        self.assertEqual(data["id"], comment.id)
        self.assertEqual(data["content"], comment.content)
        self.assertIn("date", data)
        self.assertEqual(data["user"], comment.user.id)
        self.assertEqual(data["username"], self.another_user.username)
        self.assertEqual(data["item"], comment.item.id)
        self.assertEqual(data["user_fullname"], "first2 last2")
        self.assertNotEqual(data["user_profile_picture"], None)

    def test_get_item_comments(self):
        now = timezone.now()
        c1 = Comment.objects.create(user=self.another_user, item=self.item, content="nice",
                                    date=now)
        c2 = Comment.objects.create(user=self.another_user, item=self.item, content="cool",
                                    date=now + timezone.timedelta(seconds=1))
        c3 = Comment.objects.create(user=self.another_user, item=self.item, content="fun",
                                    date=now + timezone.timedelta(seconds=2))

        r = self.client.get("%s%d/comments/" % (self.url, self.item.id))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 3)
        self.check_get_comment_data_complete(r.data[0], c3)
        self.check_get_comment_data_complete(r.data[1], c2)
        self.check_get_comment_data_complete(r.data[2], c1)


class ArchiveRestoreItemTests(ItemBaseTest):
    archive_item_url = "/api/items/%d/archive/"
    restore_item_url = "/api/items/%d/restore/"

    def setUp(self):
        super().setUp()
        self.login()

        self.item1 = Item.objects.create(name="Test1", description="Description1", owner=self.current_user,
                                         price_min=1, price_max=2, category=self.c1)
        self.item2 = Item.objects.create(name="Test2", description="Description2", owner=self.current_user,
                                         price_min=1, price_max=2, category=self.c1)
        self.item3 = Item.objects.create(name="Test3", description="Description3", owner=self.current_user,
                                         price_min=1, price_max=2, category=self.c1)
        self.item4 = Item.objects.create(name="Test3", description="Description3", owner=self.another_user,
                                         price_min=1, price_max=2, category=self.c1)

    def archive_item(self, item_id=1):
        return self.client.post(self.archive_item_url % item_id, data=json.dumps({}), content_type="application/json")

    def restore_item(self, item_id=1):
        return self.client.post(self.restore_item_url % item_id, data=json.dumps({}), content_type="application/json")

    def test_archive_item_not_logged_in(self):
        self.client.logout()

        r = self.archive_item()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restore_item_not_logged_in(self):
        self.client.logout()

        r = self.restore_item()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_archive_item(self):
        r = self.archive_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item()
        self.assertEqual(r.data["archived"], True)

    def test_cannot_archive_item_if_pending_offers_done(self):
        Offer.objects.create(item_given=self.item1, item_received=self.item4)
        r = self.archive_item()
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_archive_item_if_pending_offers_received(self):
        Offer.objects.create(item_received=self.item4, item_given=self.item1)
        r = self.archive_item()
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restore_item(self):
        self.archive_item()
        r = self.restore_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item()
        self.assertEqual(r.data["archived"], False)

    def test_archive_items(self):
        self.archive_item()
        self.archive_item(item_id=2)

        r = self.get_item()
        self.assertEqual(r.data["archived"], True)
        r = self.get_item(item_id=2)
        self.assertEqual(r.data["archived"], True)
        r = self.get_item(item_id=3)
        self.assertEqual(r.data["archived"], False)

    def test_restore_items(self):
        self.archive_item()
        self.archive_item(item_id=2)
        self.restore_item()
        self.restore_item(item_id=2)

        r = self.get_item()
        self.assertEqual(r.data["archived"], False)
        r = self.get_item(item_id=2)
        self.assertEqual(r.data["archived"], False)
        r = self.get_item(item_id=3)
        self.assertEqual(r.data["archived"], False)
