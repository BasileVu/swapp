import json

from PIL import Image as ImagePil
from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework import status

from items.models import *
from users.models import *


class CategoryTests(TestCase):
    def test_category_name_unique(self):
        Category.objects.create(name="test")
        self.assertRaises(IntegrityError, Category.objects.create, name="test")


class DeliveryMethodTests(TestCase):
    def test_delivery_method_name_unique(self):
        DeliveryMethod.objects.create(name="test")
        self.assertRaises(IntegrityError, DeliveryMethod.objects.create, name="test")


class ItemTests(TestCase):
    def test_item_creation(self):
        u = User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)

        c = Category.objects.create(name="test")
        self.assertEqual(Category.objects.count(), 1)

        Item.objects.create(name="test", description="test", price_min=1, price_max=2, archived=0, category=c, owner=u)
        self.assertEqual(Item.objects.count(), 1)


class ImageAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")

        c = Category.objects.create(name="Test")
        self.item = Item.objects.create(name="Test", description="Test", price_min=1, price_max=2, archived=False,
                                        category=c, owner=self.current_user)

        self.login()

    def login(self):
        self.client.login(username="username", password="password")

    def post_image(self, item_id=1):
        image = ImagePil.new("RGBA", size=(50, 50), color=(155, 0, 0))
        image.save("test.png")

        with open("test.png", "rb") as data:
            return self.client.post("/api/images/", {"image": data, "item": item_id}, format="multipart")

    def delete_image(self, image_id=1):
        return self.client.delete("/api/images/" + str(image_id) + "/", content_type="application/json")

    def test_post_image(self):
        self.assertEqual(Image.objects.count(), 0)

        self.login()
        r = self.post_image()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(self.item.image_set.count(), 1)
        self.assertNotEqual(self.item.image_set.first().image.name, "")
        self.assertNotEqual(self.item.image_set.first().image.url, "")

        r = self.client.get("/api/items/%s/" % self.item.id)
        self.assertEqual(r.data["images"][0]["id"], 1)
        self.assertNotEqual(r.data["images"][0]["url"], None)

    def test_post_images(self):
        self.assertEqual(Image.objects.count(), 0)

        self.login()
        self.post_image()
        self.post_image()

        self.assertEqual(Image.objects.count(), 2)
        self.assertEqual(self.item.image_set.count(), 2)

        r = self.client.get("/api/items/%s/" % self.item.id)
        self.assertEqual(r.data["images"][0]["id"], 1)
        self.assertNotEqual(r.data["images"][0]["url"], None)
        self.assertEqual(r.data["images"][1]["id"], 2)
        self.assertNotEqual(r.data["images"][1]["url"], None)

    def test_delete_image(self):
        self.login()
        r = self.post_image()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.delete_image()
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Image.objects.count(), 0)

        r = self.delete_image(image_id=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class DeliveryMethodAPITests(TestCase):
    delivery_methods_url = "/api/deliverymethods/"

    def setUp(self):
        DeliveryMethod.objects.create(name="At my place")
        DeliveryMethod.objects.create(name="At any place")
        DeliveryMethod.objects.create(name="By mail")

    def get_delivery_methods(self):
        return self.client.get(self.delivery_methods_url, content_type="application/json")

    def get_delivery_method(self, id_delivery_method=1):
        return self.client.get("%s%d/" % (self.delivery_methods_url, id_delivery_method),
                               content_type="application/json")

    def test_get_delivery_method(self):
        r = self.get_delivery_method()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["name"], "At my place")

        r = self.get_delivery_method(id_delivery_method=100)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_delivery_methods(self):
        r = self.get_delivery_methods()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 3)
        self.assertEqual(r.data[0]["id"], 1)
        self.assertEqual(r.data[0]["name"], "At my place")
        self.assertEqual(r.data[1]["id"], 2)
        self.assertEqual(r.data[1]["name"], "At any place")
        self.assertEqual(r.data[2]["id"], 3)
        self.assertEqual(r.data[2]["name"], "By mail")

    def test_post_delete_put_patch_should_not_work_delivery_method(self):
        User.objects.create_user(username="username", email="test@test.com", password="password")
        self.client.login(username="username", password="password")

        r = self.client.post(self.delivery_methods_url, data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.put("%s%d/" % (self.delivery_methods_url, 1), data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("%s%d/" % (self.delivery_methods_url, 1), data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.delete("%s%d/" % (self.delivery_methods_url, 1), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryAPITests(TestCase):
    categories_url = "/api/categories/"

    def setUp(self):
        Category.objects.create(name="Test1")
        Category.objects.create(name="Test2")

    def get_categories(self):
        return self.client.get(self.categories_url, content_type="application/json")

    def get_category(self, id_category=1):
        return self.client.get("%s%d/" % (self.categories_url, id_category), content_type="application/json")

    def test_get_category(self):
        r = self.get_category()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["name"], "Test1")

        r = self.get_category(id_category=100)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_categories(self):
        r = self.get_categories()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)
        self.assertEqual(r.data[0]["id"], 1)
        self.assertEqual(r.data[0]["name"], "Test1")
        self.assertEqual(r.data[1]["id"], 2)
        self.assertEqual(r.data[1]["name"], "Test2")

    def test_post_delete_put_patch_should_not_work_category(self):
        User.objects.create_user(username="username", email="test@test.com", password="password")
        self.client.login(username="username", password="password")

        r = self.client.post(self.categories_url, data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.put("%s%d/" % (self.categories_url, 1), data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("%s%d/" % (self.categories_url, 1), data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.delete("%s%d/" % (self.categories_url, 1), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class LikeAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")

        self.other_user = User.objects.create_user(username="user1", email="test@test.com",
                                                   password="password")

        self.create_item(c1, self.other_user, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.create_item(c2, self.current_user, name="Shirt", description="My old shirt", price_min=5,
                         price_max=30)

        self.client.login(username="username", password="password")

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def post_like(self, item):
        return self.client.post("/api/likes/", data=json.dumps({
            "item": item
        }), content_type="application/json")

    def get_likes(self):
        return self.client.get("/api/likes/", content_type="application/json")

    def get_like(self, id_like):
        return self.client.get("/api/likes/%d/" % id_like, content_type="application/json")

    def delete_like(self, id_like):
        return self.client.delete("/api/likes/%d/" % id_like, content_type="application/json")

    def test_post_like(self):
        r = self.post_like(1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["user"], "username")
        self.assertEqual(r.data["item"], 1)
        self.assertIn("date", r.data)

    def test_cannot_like_own_item(self):
        r = self.post_like(2)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_like_an_item_twice(self):
        self.post_like(1)
        r = self.post_like(1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_likes_no_likes(self):
        r = self.get_likes()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_get_likes_1_like(self):
        self.post_like(1)

        r = self.get_likes()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["id"], 1)
        self.assertEqual(r.data[0]["user"], "username")
        self.assertEqual(r.data[0]["item"], 1)
        self.assertIn("date", r.data[0])

    def test_get_like(self):
        r = self.post_like(1)
        r = self.get_like(id_like=r.data["id"])

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["user"], "username")
        self.assertEqual(r.data["item"], 1)
        self.assertIn("date", r.data)

    def test_get_like_404(self):
        r = self.get_like(id_like=1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_like(self):
        r = self.post_like(1)
        r = self.delete_like(id_like=r.data["id"])
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.delete_like(id_like=1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_patch_should_be_denied(self):
        r = self.client.put("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
