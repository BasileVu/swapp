from django.test import TestCase
from rest_framework import status

from items.models import *
from users.models import *


class ItemListTests(TestCase):
    url = "/api/items/"

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def setUp(self):
        u1 = User.objects.create_user(username="user1", email="test@test.com", password="password")
        u2 = User.objects.create_user(username="user2", email="test2@test.com", password="password")
        u3 = User.objects.create_user(username="user3", email="test3@test.com", password="password")

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

        u3.coordinates.latitude = self.latitude
        u3.coordinates.longitude = self.longitude
        u3.coordinates.save()

        c1 = Category.objects.create(name="Test")
        c2 = Category.objects.create(name="Test2")
        c3 = Category.objects.create(name="Test3")

        self.c = c1

        self.item1 = self.create_item(c1, u1, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.item2 = self.create_item(c2, u1, name="Shirt", description="My old shirt", price_min=5, price_max=30)
        self.item3 = self.create_item(c3, u1, name="Ring", description="My precious", price_min=100, price_max=500)
        self.item4 = self.create_item(c1, u2, name="New mouse", description="Brand new", price_min=20, price_max=100)
        self.item5 = self.create_item(c2, u2, name="Piano", description="Still nice to the ear", price_min=500,
                                      price_max=1000)

        self.client.login(username="user3", password="password")

    def test_suggestions_far_away_should_be_last(self):
        u = User.objects.create_user(username="user4", email="test4@test.com", password="password")
        u.coordinates.latitude = 0
        u.coordinates.longitude = 0
        u.coordinates.save()
        item = self.create_item(self.c, u, name="Should be last", description="", price_min=10, price_max=30)

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 6)

        self.assertEquals(r.data[0]["name"], self.item4.name)
        self.assertEquals(r.data[1]["name"], self.item5.name)
        self.assertEquals(r.data[2]["name"], self.item1.name)
        self.assertEquals(r.data[3]["name"], self.item2.name)
        self.assertEquals(r.data[4]["name"], self.item3.name)
        self.assertEquals(r.data[5]["name"], item.name)

    def test_suggestions_no_archived_items(self):
        i = Item.objects.get(id=1)
        i.archived = True
        i.save()

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 4)

    def test_list_item_no_archived_item(self):
        i = Item.objects.get(id=1)
        i.archived = True
        i.save()

        r = self.client.get(self.url + "?q=")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 4)

    def test_suggestions_no_own_item(self):
        self.client.logout()
        self.client.login(username="user1", password="password")

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_list_no_own_item(self):
        self.client.logout()
        self.client.login(username="user1", password="password")

        r = self.client.get(self.url + "?q=")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_list_item_q(self):
        r = self.client.get(self.url + "?q=my")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 3)

        r = self.client.get(self.url + "?q=shoes")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?q=sh")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_list_item_category_not_existing(self):
        r = self.client.get(self.url + "?category=category")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?category=test")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_list_item_category(self):
        r = self.client.get(self.url + "?category=Test")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?category=Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?category=Test3")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_list_item_price_min_lower_bound(self):
        r = self.client.get(self.url + "?price_min=0")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_min=5")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

    def test_list_item_price_min(self):
        r = self.client.get(self.url + "?price_min=10")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 4)

    def test_list_item_price_min_upper_bound(self):
        r = self.client.get(self.url + "?price_min=1000")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_list_item_price_max_lower_bound(self):
        r = self.client.get(self.url + "?price_max=5")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_list_item_price_max(self):
        r = self.client.get(self.url + "?price_max=30")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_list_item_price_max_upper_bound(self):
        r = self.client.get(self.url + "?price_max=1000")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

        r = self.client.get(self.url + "?price_max=10000")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

    def test_list_item_no_matching_for_price_range(self):
        r = self.client.get(self.url + "?price_min=0&price_max=0")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=0&price_max=5")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.url + "?price_min=5&price_max=5")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_list_item_price_range(self):
        r = self.client.get(self.url + "?price_min=5&price_max=30")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

        r = self.client.get(self.url + "?price_min=10&price_max=30")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=500&price_max=10000")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

        r = self.client.get(self.url + "?price_min=0&price_max=1000")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

    def test_list_item_latitude_longitude(self):
        r = self.client.get(self.url + "?lat=%f&lon=%f" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 5)

    def test_list_item_latitude_longitude_radius(self):
        r = self.client.get(self.url + "?lat=%f&lon=%f&radius=1" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_list_item_latitude_longitude_radius_too_small(self):
        r = self.client.get(self.url + "?lat=%f&lon=%f&radius=0.1" % (self.latitude, self.longitude))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 0)

    def test_wrong_parameter_format(self):
        r = self.client.get(self.url + "?price_min=test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.client.get(self.url + "?price_max=test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.client.get(self.url + "?lat=test&lon=test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.client.get(self.url + "?lat=test&lon=test&radius=test")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_by_name(self):
        r = self.client.get(self.url + "?order_by=name")
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item4.name)
        self.assertEquals(r.data[1]["name"], self.item5.name)
        self.assertEquals(r.data[2]["name"], self.item3.name)
        self.assertEquals(r.data[3]["name"], self.item2.name)
        self.assertEquals(r.data[4]["name"], self.item1.name)

    def test_order_by_category(self):
        r = self.client.get(self.url + "?order_by=category")
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item1.name)
        self.assertEquals(r.data[1]["name"], self.item4.name)
        self.assertEquals(r.data[2]["name"], self.item2.name)
        self.assertEquals(r.data[3]["name"], self.item5.name)
        self.assertEquals(r.data[4]["name"], self.item3.name)

    def test_order_by_price_min(self):
        r = self.client.get(self.url + "?order_by=price_min")
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item2.name)
        self.assertEquals(r.data[1]["name"], self.item1.name)
        self.assertEquals(r.data[2]["name"], self.item4.name)
        self.assertEquals(r.data[3]["name"], self.item3.name)
        self.assertEquals(r.data[4]["name"], self.item5.name)

    def test_order_by_price_max(self):
        r = self.client.get(self.url + "?order_by=price_max")
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item5.name)
        self.assertEquals(r.data[1]["name"], self.item3.name)
        self.assertEquals(r.data[2]["name"], self.item4.name)
        self.assertEquals(r.data[3]["name"], self.item1.name)
        self.assertEquals(r.data[4]["name"], self.item2.name)

    def test_order_by_range(self):
        r = self.client.get(self.url + "?lat=%f&lon=%f&order_by=range" % (self.latitude, self.longitude))
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item4.name)
        self.assertEquals(r.data[1]["name"], self.item5.name)
        self.assertEquals(r.data[2]["name"], self.item1.name)
        self.assertEquals(r.data[3]["name"], self.item2.name)
        self.assertEquals(r.data[4]["name"], self.item3.name)

    def test_order_by_date(self):
        now = timezone.now()

        self.item3.creation_date = now
        self.item2.creation_date = now + timezone.timedelta(seconds=1)
        self.item1.creation_date = now + timezone.timedelta(seconds=2)
        self.item4.creation_date = now + timezone.timedelta(seconds=3)
        self.item5.creation_date = now + timezone.timedelta(seconds=4)

        self.item1.save()
        self.item2.save()
        self.item3.save()
        self.item4.save()
        self.item5.save()

        r = self.client.get(self.url + "?order_by=date")
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(r.data[0]["name"], self.item3.name)
        self.assertEquals(r.data[1]["name"], self.item2.name)
        self.assertEquals(r.data[2]["name"], self.item1.name)
        self.assertEquals(r.data[3]["name"], self.item4.name)
        self.assertEquals(r.data[4]["name"], self.item5.name)

    def test_all_filters(self):
        r = self.client.get(self.url +
                            "?q=s"
                            "&category=Test"
                            "&price_min=5"
                            "&price_max=30"
                            "&lat=%f&lon=%f&radius=10"
                            "&order_by=name"
                            % (self.latitude, self.longitude))
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(len(r.data), 1)
        self.assertEquals(r.data[0]["name"], self.item1.name)

        r = self.client.get(self.url +
                            "?q=s"
                            "&category=Test2"
                            "&price_min=5"
                            "&price_max=30"
                            "&lat=%f&lon=%f&radius=10"
                            "&order_by=name"
                            % (self.latitude, self.longitude))
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(len(r.data), 1)
        self.assertEquals(r.data[0]["name"], self.item2.name)

        r = self.client.get(self.url +
                            "?q=s"
                            "&category=Test"
                            "&price_min=5"
                            "&price_max=100"
                            "&lat=%f&lon=%f&radius=1"
                            "&order_by=name"
                            % (self.latitude, self.longitude))
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertEquals(len(r.data), 1)
        self.assertEquals(r.data[0]["name"], self.item4.name)
