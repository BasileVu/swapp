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
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        c = Category.objects.create(name="Test")
        Item.objects.create(name="Test", description="Test", price_min=1, price_max=2, archived=False, category=c,
                            owner=self.current_user)

        self.login()

    def login(self):
        self.client.login(username="username", password="password")

    def post_image(self, item):
        image = ImagePil.new('RGBA', size=(50, 50), color=(155, 0, 0))
        #file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save('test.png')

        with open('test.png', 'rb') as data:
            return self.client.post("/api/images/", {"image": data, "item": item}, format='multipart')

    def get_image(self, id_image=1):
        return self.client.get("/api/images/" + str(id_image) + "/", content_type="application/json")

    def delete_image(self, id_image=1):
        return self.client.delete("/api/images/" + str(id_image) + "/", content_type="application/json")

    def test_post_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_get_image(self):
        r = self.get_image()
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(r.data), 1)

        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_image()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 3)

    def test_post_get_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_image(id_image=1)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_image(id_image=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_patch_should_be_denied_offer(self):
        self.login()

        r = self.client.put("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Image.objects.count(), 1)

        r = self.delete_image(id_image=1)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Image.objects.count(), 0)

        r = self.delete_image(id_image=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class CategoryAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.save()

        Category.objects.create(name="Test")
        Category.objects.create(name="Test2")

        self.login()

    def login(self):
        self.client.login(username="username", password="password")

    def get_categories(self):
        return self.client.get("/api/categories/", content_type="application/json")

    def get_category(self, id_category=1):
        return self.client.get("/api/categories/" + str(id_category) + "/", content_type="application/json")

    def test_get_categories(self):
        r = self.get_categories()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_get_category(self):
        r = self.get_category(id_category=1)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_category(id_category=100)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_delete_put_patch_should_not_work_category(self):
        self.login()

        r = self.client.post("/api/categories/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.put("/api/categories/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("/api/categories/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.delete("/api/categories/1/", content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class LikeAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")

        self.other_user = User.objects.create_user(username="user1", email="test@test.com",
                                                   password="password")

        self.create_item(c1, self.other_user, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.create_item(c2, self.current_user, name="Shirt", description="My old shirt", price_min=5,
                         price_max=30)

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def login(self):
        self.client.login(username="username", password="password")

    def post_like(self, user, item):
        return self.client.post("/api/likes/", data=json.dumps({
            "user": user,
            "item": item
        }), content_type="application/json")

    def get_likes(self):
        return self.client.get("/api/likes/", content_type="application/json")

    def get_like(self, id_like):
        return self.client.get("/api/likes/" + str(id_like) + "/", content_type="application/json")

    def delete_like(self, id_like):
        return self.client.delete("/api/items/" + str(id_like) + "/", content_type="application/json")

    def test_post_like(self):
        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_get_likes(self):
        r = self.get_likes()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_likes()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_get_like(self):
        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_like(id_like=r.data['id'])
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_like(id_like=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_like(self):
        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        id_item = r.data['id']
        r = self.get_likes()
        self.assertEqual(len(r.data), 1)

        r = self.delete_like(id_like=id_item)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = self.get_likes()
        self.assertEqual(len(r.data), 0)

        r = self.delete_like(id_like=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_patch_should_be_denied(self):
        self.login()

        r = self.client.put("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        r = self.client.patch("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
