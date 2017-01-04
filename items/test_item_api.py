import json

from PIL import Image as ImagePil
from django.test import TestCase
from rest_framework import status

from comments.models import *
from items.models import *
from users.models import *


class ItemAPITests(TestCase):
    url = "/api/items/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")

        self.c1 = Category.objects.create(name="test")
        self.c2 = Category.objects.create(name="test2")

    def login(self):
        self.client.login(username="username", password="password")

    def post_item(self, name="name", description="description", price_min=1, price_max=2, category=1):
        return self.client.post(self.url, data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category
        }), content_type="application/json")

    def get_items(self):
        return self.client.get(self.url, content_type="application/json")

    def get_item(self, id_item=1):
        return self.client.get(self.url + str(id_item) + "/", content_type="application/json")

    def put_item(self, id_item=1, name="name", description="description", price_min=1, price_max=2, category=1):
        return self.client.put(self.url + str(id_item) + "/", data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
        }), content_type="application/json")

    def delete_item(self, id_item=1):
        return self.client.delete(self.url + str(id_item) + "/", content_type="application/json")

    def patch_item(self, id_item=1, data=json.dumps({"name": "test"})):
        return self.client.patch(self.url + str(id_item) + "/", data=data, content_type="application/json")

    def post_image(self, user_id):
        image = ImagePil.new("RGBA", size=(50, 50), color=(155, 0, 0))
        image.save("test.png")

        with open("test.png", "rb") as data:
            return self.client.post("/api/images/", {"image": data, "user": user_id}, format="multipart")

    def test_post_item_not_logged_in(self):
        r = self.post_item()
        self.assertEqual(r.status_code, 401)

    def test_post_item_logged_in(self):
        self.login()

        r = self.post_item()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_post_item_price_min_bigger_than_price_max(self):
        self.login()

        r = self.post_item(price_min=2, price_max=1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Item.objects.count(), 0)

    def test_post_item_json_data_invalid(self):
        self.login()

        r = self.client.post(self.url, data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_items(self):
        r = self.get_items()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

        self.login()
        r = self.post_item()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        r = self.get_items()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_get_item(self):
        self.login()

        r = self.post_item()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item(id_item=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_item_not_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        id_item = r.data['id']
        r = self.put_item(id_item=id_item, name="test2", description="test2", price_min=2, price_max=3, category=2)
        self.assertEqual(r.status_code, 401)

    def test_put_item_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        id_item = r.data['id']
        r = self.put_item(id_item=id_item, name="test2", description="test2", price_min=2, price_max=3, category=2)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category']['name'], "test2")

        r = self.put_item(id_item=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_item_not_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        id_item = r.data['id']
        r = self.patch_item(id_item=id_item, data=json.dumps({"name": "test2"}))
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_item_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        id_item = r.data['id']
        r = self.patch_item(id_item=id_item, data=json.dumps({"name": "test2"}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.patch_item(id_item=id_item, data=json.dumps({"description": "test2"}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.patch_item(id_item=id_item, data=json.dumps({"price_min": 2}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.patch_item(id_item=id_item, data=json.dumps({"price_max": 3}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.patch_item(id_item=id_item, data=json.dumps({"category": 2}))
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category']['name'], "test2")

        r = self.patch_item(id_item=10)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_set_min_price_greater_than_max_price(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)

        id = r.data["id"]
        r = self.patch_item(id_item=id, data=json.dumps({"price_min": 3}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.get_item(id_item=id)
        self.assertEquals(r.data['price_min'], 1)

    def test_cannot_set_max_price_smaller_than_min_price(self):
        self.login()
        r = self.post_item(price_min=1, price_max=2)

        id = r.data["id"]
        r = self.patch_item(id_item=id, data=json.dumps({"price_max": 0}))
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.get_item(id_item=id)
        self.assertEquals(r.data['price_max'], 2)

    def test_delete_item_not_logged_in(self):
        self.login()
        r = self.post_item(price_min=1, price_max=2)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.client.logout()

        id_item = r.data['id']
        r = self.get_items()
        self.assertEqual(len(r.data), 1)

        r = self.delete_item(id_item=id_item)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_item_values_for_list_and_get_testing(self):
        u = User.objects.create_user(username="username2", password="password")
        i = Item.objects.create(owner=self.current_user, name="test", description="test", price_min=1, price_max=2,
                                category=self.c1)
        Like.objects.create(user=u, item=i)

    def check_get_item_data_complete(self, data):
        self.assertEqual(data["owner_username"], "username")
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["description"], "test")
        self.assertEqual(data["price_min"], 1)
        self.assertEqual(data["price_max"], 2)
        self.assertIn("creation_date", data)
        self.assertEqual(data["category"]['id'], 1)
        self.assertEqual(data["category"]['name'], "test")
        self.assertEqual(data["views"], 1)
        self.assertEqual(data["comments"], 0)
        self.assertEqual(data["likes"], 1)
        self.assertIn("image_urls", data)

    def test_get_items_result(self):
        self.create_item_values_for_list_and_get_testing()
        item = Item.objects.get(pk=1)
        item.views = 1
        item.save()

        r = self.get_items()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_item_data_complete(r.data[0])

    def test_get_item_result(self):
        self.create_item_values_for_list_and_get_testing()

        r = self.get_item(1)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.check_get_item_data_complete(r.data)

    def test_get_item_should_increment_views(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['views'], 1)

        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['views'], 2)

    def test_get_item_comments(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.client.logout()

        u = User.objects.create_user(first_name="firstName", last_name="lastName", username="username2",
                                     password="password")
        self.client.login(username="username2", password="password")
        self.post_image(u.id)
        self.client.logout()

        item = Item.objects.get(pk=r.data["id"])

        c1 = Comment.objects.create(user=u, item=item, content="nice")
        Comment.objects.create(user=u, item=item, content="cool")
        Comment.objects.create(user=u, item=item, content="fun")

        r = self.client.get("/api/items/%d/comments/" % r.data["id"])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 3)
        self.assertEqual(r.data[0]["id"], c1.id)
        self.assertEqual(r.data[0]["content"], c1.content)
        self.assertIn("date", r.data[0])
        self.assertEqual(r.data[0]["user"], c1.user.id)
        self.assertEqual(r.data[0]["item"], c1.item.id)
        self.assertEqual(r.data[0]["user_fullname"], "firstName lastName")
        self.assertNotEqual(r.data[0]["user_profile_picture"], None)

    '''
    def test_archive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.c.patch("/api/items/1/archive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_unarchive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.c.patch("/api/items/1/unarchive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
    '''
