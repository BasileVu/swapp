import json

from PIL import Image as ImagePil
from django.test import TestCase

from items.models import *
from swapp.gmaps_api_utils import compute_distance
from users.models import *


class ItemTests(TestCase):
    def test_item_creation(self):
        u = User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)

        c = Category.objects.create(name="test")
        self.assertEqual(Category.objects.count(), 1)

        Item.objects.create(name="test", description="test", price_min=1, price_max=2, archived=0, category=c, owner=u)
        self.assertEqual(Item.objects.count(), 1)


class ItemAPITests(TestCase):
    url = "/api/items/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.save()

        Category.objects.create(name="test")
        Category.objects.create(name="test2")

    def login(self):
        self.client.login(username="username", password="password")

    def post_item(self, name="name", description="description", price_min=1, price_max=2, category=1, image_set=list(),
                  like_set=list()):
        return self.client.post(self.url, data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "image_set": image_set,
            "like_set": like_set
        }), content_type="application/json")

    def post_like(self, user, item):
        return self.client.post("/api/likes/", data=json.dumps({
            "user": user,
            "item": item
        }), content_type="application/json")

    def post_image(self, item):
        image = ImagePil.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save('test.png')

        with open('test.png', 'rb') as data:
            return self.client.post("/api/images/", {"image": data, "item": item}, format='multipart')

    def get_items(self):
        return self.client.get(self.url, content_type="application/json")

    def get_item(self, id_item=1):
        return self.client.get(self.url + str(id_item) + "/", content_type="application/json")

    def put_item(self, id_item=1, name="name", description="description", price_min=1, price_max=2, category=1,
                 image_set=list(), like_set=list()):
        return self.client.put(self.url + str(id_item) + "/", data=json.dumps({
            "name": name,
            "description": description,
            "price_min": price_min,
            "price_max": price_max,
            "category": category,
            "image_set": image_set,
            "like_set": like_set
        }), content_type="application/json")

    def delete_item(self, id_item=1):
        return self.client.delete(self.url + str(id_item) + "/", content_type="application/json")

    def patch_item(self, id_item=1, data=json.dumps({"name": "test"})):
        return self.client.patch(self.url + str(id_item) + "/", data=data, content_type="application/json")

    def test_post_item_not_logged_in(self):
        r = self.post_item()
        self.assertEqual(r.status_code, 401)

    def test_post_item_logged_in(self):
        self.login()

        r = self.post_item()
        self.assertEqual(r.status_code, 201)

    def test_post_item_price_min_bigger_than_price_max(self):
        self.login()

        r = self.post_item(price_min=2, price_max=1)
        self.assertEqual(r.status_code, 400)

    def test_post_item_json_data_invalid(self):
        self.login()

        r = self.client.post(self.url, data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_get_items(self):
        r = self.get_items()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        self.login()
        r = self.post_item()
        self.assertEqual(r.status_code, 201)

        r = self.get_items()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_get_item(self):
        self.login()

        r = self.post_item()
        self.assertEqual(r.status_code, 201)
        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, 200)

        r = self.get_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_put_item_not_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        self.client.logout()

        id_item = r.data['id']
        r = self.put_item(id_item=id_item, name="test2", description="test2", price_min=2, price_max=3, category=2)
        self.assertEqual(r.status_code, 401)

    def test_put_item_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)

        id_item = r.data['id']
        r = self.put_item(id_item=id_item, name="test2", description="test2", price_min=2, price_max=3, category=2)
        self.assertEqual(r.status_code, 200)

        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category']['name'], "test2")

        r = self.put_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_patch_item_not_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        self.client.logout()

        id_item = r.data['id']
        r = self.patch_item(id_item=id_item, data=json.dumps({"name": "test2"}))
        self.assertEqual(r.status_code, 401)

    def test_patch_item_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)

        id_item = r.data['id']
        r = self.patch_item(id_item=id_item, data=json.dumps({"name": "test2"}))
        self.assertEqual(r.status_code, 200)

        r = self.patch_item(id_item=id_item, data=json.dumps({"description": "test2"}))
        self.assertEqual(r.status_code, 200)

        r = self.patch_item(id_item=id_item, data=json.dumps({"price_min": 2}))
        self.assertEqual(r.status_code, 200)

        r = self.patch_item(id_item=id_item, data=json.dumps({"price_max": 3}))
        self.assertEqual(r.status_code, 200)

        r = self.patch_item(id_item=id_item, data=json.dumps({"category": 2}))
        self.assertEqual(r.status_code, 200)

        r = self.get_item(id_item=id_item)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "test2")
        self.assertEqual(r.data['description'], "test2")
        self.assertEqual(r.data['price_min'], 2)
        self.assertEqual(r.data['price_max'], 3)
        self.assertEqual(r.data['category']['name'], "test2")

        r = self.patch_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_delete_item_not_logged_in(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)
        self.client.logout()

        id_item = r.data['id']
        r = self.get_items()
        self.assertEqual(len(r.data), 1)

        r = self.delete_item(id_item=id_item)
        self.assertEqual(r.status_code, 401)

    def test_delete_item(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)

        id_item = r.data['id']
        r = self.get_items()
        self.assertEqual(len(r.data), 1)

        r = self.delete_item(id_item=id_item)
        self.assertEqual(r.status_code, 204)

        r = self.get_items()
        self.assertEqual(len(r.data), 0)

        r = self.delete_item(id_item=10)
        self.assertEqual(r.status_code, 404)

    def test_get_items_should_return_like_set_category_name_and_image_set_with_name(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)

        r = self.post_like(1, 1)
        self.assertEqual(r.status_code, 201)

        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

        r = self.get_items()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1);
        self.assertEqual(r.data[0]['name'], "test")
        self.assertEqual(r.data[0]['description'], "test")
        self.assertEqual(r.data[0]['price_min'], 1)
        self.assertEqual(r.data[0]['price_max'], 2)
        self.assertEqual(r.data[0]['category']['name'], "test")
        self.assertIn("/media/test", r.data[0]['image_set'][0]["image"])
        self.assertEqual(r.data[0]['like_set'][0]["user"], 1)

    def test_get_item_should_return_like_set_category_name_and_image_set_with_name(self):
        self.login()
        r = self.post_item(name="test", description="test", price_min=1, price_max=2, category=1)
        self.assertEqual(r.status_code, 201)

        r = self.post_like(1, 1)
        self.assertEqual(r.status_code, 201)

        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

        r = self.get_item(id_item=r.data['id'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "test")
        self.assertEqual(r.data['description'], "test")
        self.assertEqual(r.data['price_min'], 1)
        self.assertEqual(r.data['price_max'], 2)
        self.assertEqual(r.data['category']['name'], "test")
        self.assertIn("/media/test", r.data['image_set'][0]["image"])
        self.assertEqual(r.data['like_set'][0]["user"], 1)

    # FIXME
    '''
    def test_post_item_user_location_not_specified(self):
        self.current_user.userprofile.location = ""
        self.current_user.userprofile.save()
        r = self.post_item()
        self.assertEqual(r.status_code, 400)
    '''
    '''
    def test_archive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 201)
        r = self.c.patch("/api/items/1/archive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 200)

    def test_unarchive_item(self):
        r = self.c.post("/api/items/", data=json.dumps({
            "name": "test",
            "description": "test",
            "price_min": 1,
            "price_max": 2,
            "category": 1
        }), content_type="application/json")
        self.assertEqual(r.status_code, 201)
        r = self.c.patch("/api/items/1/unarchive", data=json.dumps({}), content_type="application/json")
        self.assertEqual(r.status_code, 200)
    '''


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

    def get_images(self):
        return self.client.get("/api/images/", content_type="application/json")

    def get_image(self, id_image=1):
        return self.client.get("/api/images/" + str(id_image) + "/", content_type="application/json")

    def delete_image(self, id_image=1):
        return self.client.delete("/api/images/" + str(id_image) + "/", content_type="application/json")

    def test_post_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

    def test_get_image(self):
        r = self.get_image()
        self.assertEqual(r.status_code, 404)
        self.assertEqual(len(r.data), 1)

        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

        r = self.get_image()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 3)

    def test_post_get_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

        r = self.get_image(id_image=r.data['id'])
        self.assertEqual(r.status_code, 200)

        r = self.get_image(id_image=10)
        self.assertEqual(r.status_code, 404)

    def test_put_patch_should_be_denied_offer(self):
        self.login()

        r = self.client.put("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

        r = self.client.patch("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

    def test_delete_image(self):
        self.login()
        r = self.post_image(1)
        self.assertEqual(r.status_code, 201)

        id_image = r.data['id']
        r = self.get_images()
        self.assertEqual(len(r.data), 1)

        r = self.delete_image(id_image=id_image)
        self.assertEqual(r.status_code, 204)

        r = self.get_images()
        self.assertEqual(len(r.data), 0)

        r = self.delete_image(id_image=10)
        self.assertEqual(r.status_code, 404)


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
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

    def test_get_category(self):
        r = self.get_category(id_category=1)
        self.assertEqual(r.status_code, 200)

        r = self.get_category(id_category=100)
        self.assertEqual(r.status_code, 404)

    def test_post_delete_put_patch_should_not_work_category(self):
        self.login()

        r = self.client.post("/api/categories/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

        r = self.client.put("/api/categories/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

        r = self.client.patch("/api/categories/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

        r = self.client.delete("/api/categories/1/", content_type="application/json")
        self.assertEqual(r.status_code, 405)


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
        self.assertEqual(r.status_code, 201)

    def test_get_likes(self):
        r = self.get_likes()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, 201)

        r = self.get_likes()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_get_like(self):
        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, 201)

        r = self.get_like(id_like=r.data['id'])
        self.assertEqual(r.status_code, 200)

        r = self.get_like(id_like=10)
        self.assertEqual(r.status_code, 404)

    def test_delete_like(self):
        self.login()
        r = self.post_like(1, self.current_user.userprofile.id)
        self.assertEqual(r.status_code, 201)

        id_item = r.data['id']
        r = self.get_likes()
        self.assertEqual(len(r.data), 1)

        r = self.delete_like(id_like=id_item)
        self.assertEqual(r.status_code, 204)

        r = self.get_likes()
        self.assertEqual(len(r.data), 0)

        r = self.delete_like(id_like=10)
        self.assertEqual(r.status_code, 404)

    def test_put_patch_should_be_denied(self):
        self.login()

        r = self.client.put("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)

        r = self.client.patch("/api/likes/1/", data=json.dumps({
            "name": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 405)


class ItemSearchApiTests(TestCase):
    url = "/api/items/"

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def setUp(self):
        u1 = User.objects.create_user(username="user1", email="test@test.com", password="password")
        u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password")

        # Cheseaux
        u1.coordinates.latitude = 46.7793801
        u1.coordinates.longitude = 6.659497600000001
        u1.coordinates.save()

        # St-Roch
        u2.coordinates.latitude = 46.7812274
        u2.coordinates.longitude = 6.6473097
        u2.coordinates.save()

        # Maison d'ailleurs
        self.latitude = 46.77866239999999
        self.longitude = 6.6419655

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")
        c3 = Category.objects.create(name="Test3")

        self.create_item(c1, u1, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.create_item(c2, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30)
        self.create_item(c3, u1, name="Ring", description="My precious", price_min=100, price_max=500)
        self.create_item(c1, u2, name="New mouse", description="Brand new", price_min=20, price_max=100)
        self.create_item(c2, u2, name="Piano", description="Still nice to the ear", price_min=500, price_max=1000)

    def test_list_item_no_filter(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

    def test_list_item_category(self):
        r = self.client.get(self.url + "?category=category")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?category=test")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?category=Test")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?category=Test2")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?category=Test3")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_list_item_q(self):
        r = self.client.get(self.url + "?q=my")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 3)

        r = self.client.get(self.url + "?q=shoes")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?q=sh")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

    def test_list_item_price_min(self):
        r = self.client.get(self.url + "?price_min=0")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_min=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_min=10")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 4)

        r = self.client.get(self.url + "?price_min=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

    def test_list_item_price_max(self):
        r = self.client.get(self.url + "?price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?price_max=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_max=10000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

    def test_list_item_price_range(self):
        r = self.client.get(self.url + "?price_min=0&price_max=0")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=0&price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=5&price_max=5")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=5&price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?price_min=10&price_max=30")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=500&price_max=10000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=0&price_max=1000")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

    def test_list_item_latitude_longitude_radius(self):
        r = self.client.get(self.url + "?lat=%f&lon=%f" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?lat=%f&lon=%f&radius=1" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?lat=%f&lon=%f&radius=0.1" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 0)

    def test_wrong_parameter_format(self):
        r = self.client.get(self.url + "?price_min=test")
        self.assertEqual(r.status_code, 400)

        r = self.client.get(self.url + "?price_max=test")
        self.assertEqual(r.status_code, 400)

        r = self.client.get(self.url + "?lat=test&lon=test")
        self.assertEqual(r.status_code, 400)

        r = self.client.get(self.url + "?lat=test&lon=test&radius=test")
        self.assertEqual(r.status_code, 400)
