import json
from unittest.mock import patch

from django.test import Client, TestCase
from rest_framework import status

from items.models import *
from swapp import settings
from swapp.gmaps_api_utils import OverQueryLimitError
from users.models import *


def raise_over_query_limit_error(_):
    raise OverQueryLimitError()


class UserProfileTests(TestCase):
    def test_user_profile_creation_after_user_creation(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_no_user_profile_creation_after_user_edit(self):
        u = User.objects.create_user("username", "test@test.com", "password")
        u.username = "username2"
        u.save()
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_deletion_on_user_deletion(self):
        u = User.objects.create_user("username", "test@test.com", "password")
        u.delete()
        self.assertEqual(UserProfile.objects.count(), 0)


class AccountCreationAPITests(TestCase):
    users_url = "/api/users/"

    def post_user(self, username="username", first_name="first_name", last_name="last_name", email="test@test.com",
                  password="password", password_confirmation="password",
                  street="Route de Cheseaux 1", city="Yverdon-les-Bains", region="VD", country="Switzerland"):
        return self.client.post(self.users_url, data=json.dumps({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "password_confirmation": password_confirmation,
            "street": street,
            "city": city,
            "region": region,
            "country": country
        }), content_type="application/json")

    def setUp(self):
        self.patcher = patch("users.views.get_coordinates")
        self.get_coordinates_mock = self.patcher.start()
        self.get_coordinates_mock.return_value = [{"lat": 46.7793801, "lng": 6.659497600000001}]

    def tearDown(self):
        self.patcher.stop()

    def test_user_creation(self):
        r = self.post_user()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r["Location"], "%s%s/" % (self.users_url, "username"))

        u = User.objects.get(pk=1)
        self.assertEqual(u.location.street, "Route de Cheseaux 1")
        self.assertEqual(u.location.city, "Yverdon-les-Bains")
        self.assertEqual(u.location.region, "VD")
        self.assertEqual(u.location.country, "Switzerland")

    def test_user_creation_conflict(self):
        self.post_user()
        r = self.post_user()
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

    def test_user_creation_incomplete_json(self):
        r = self.client.post(self.users_url, data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_empty_json(self):
        r = self.post_user(username="", first_name="", last_name="", email="", password="")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_password_should_match(self):
        r = self.post_user(password="password", password_confirmation="pass")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_creation_location_not_existing(self):
        self.get_coordinates_mock.return_value = []

        r = self.post_user(street="street", city="city", region="region", country="country")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_creation_over_query(self):
        self.get_coordinates_mock.side_effect = raise_over_query_limit_error
        r = self.post_user()
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class AccountConnectionAPITests(TestCase):
    login_url = "/api/login/"
    logout_url = "/api/logout/"

    def login(self, username="username", password="password"):
        return self.client.post(self.login_url, data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json")

    def setUp(self):
        User.objects.create_user(username="username", password="password")

    def test_login_incorrect(self):
        r = self.login(username="username", password="passwor")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_incomplete_json(self):
        r = self.client.post(self.login_url, data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_emtpy_json(self):
        r = self.login(username="", password="")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        r = self.login()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_not_logged_in(self):
        r = self.client.get(self.logout_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_logged_in(self):
        self.login()

        r = self.client.get(self.logout_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)


class AccountAPITests(TestCase):
    login_url = "/api/login/"
    logout_url = "/api/logout/"
    account_url = "/api/account/"

    def login(self, username="username", password="password"):
        return self.client.post(self.login_url, data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json")

    def post_image(self, image_name="test.png"):
        with open("%s/%s" % (settings.MEDIA_TEST, image_name), "rb") as data:
            return self.client.post("%s%s/" % (self.account_url, "image"), {"image": data}, format="multipart")

    def patch_interested_by_categories(self, interested_by=[]):
        return self.client.patch("%s%s/" % (self.account_url, "categories"), data=json.dumps({
            "interested_by": interested_by
        }), content_type="application/json")

    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password", first_name="first_name",
                                             last_name="last_name", email="test@test.com")
        self.login()

    def test_get_account_info_not_logged_in(self):
        self.client.logout()
        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account_info_logged_in(self):
        c = Category.objects.create(name="category")
        i = Item.objects.create(owner=self.user, category=c, price_min=50, price_max=60, )
        o = Offer.objects.create(accepted=True, answered=True, item_given=i, item_received=i)
        Note.objects.create(user=self.user, offer=o, text="test", note=4)
        Like.objects.create(user=self.user, item=i)

        self.user.userprofile.categories.add(c)
        self.user.coordinates.latitude = 4
        self.user.coordinates.longitude = 4
        self.user.coordinates.save()

        r = self.client.get(self.account_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["profile_picture_url"], None)
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["email"], "test@test.com")
        self.assertEqual(r.data["location"], {
            "street": "",
            "city": "",
            "country": "",
            "region": ""
        })
        self.assertNotEqual(r.data["last_modification_date"], "")
        self.assertEqual(r.data["categories"], [{"id": 1, "name": "category"}])
        self.assertEqual(r.data["items"], [1])
        self.assertEqual(r.data["notes"], 1)
        self.assertEqual(r.data["note_avg"], 4)
        self.assertEqual(r.data["coordinates"], {"latitude": 4, "longitude": 4})
        self.assertEqual(r.data["pending_offers"], [])

    def test_cannot_update_account_if_not_logged_in(self):
        self.client.logout()
        r = self.client.patch(self.account_url, data=json.dumps({"first_name": "f"}), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_account_logged_in(self):
        r = self.client.patch(self.account_url, data=json.dumps({"first_name": "firstname"}),
                              content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["first_name"], "firstname")

    def test_cannot_connect_if_account_not_active(self):
        self.client.logout()

        u = User.objects.get(pk=1)
        u.is_active = False
        u.save()

        r = self.client.post(self.login_url, data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_account_empty_username(self):
        r = self.client.patch(self.account_url, data=json.dumps({
            "username": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trying_to_update_last_modification_date_should_not_change_it(self):
        datetime = str(timezone.now())

        self.client.patch(self.account_url, data=json.dumps({
            "last_modification_date": datetime,
        }), content_type="application/json")
        r = self.client.get(self.account_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(r.data["last_modification_date"], datetime)

    def test_update_account_field_not_existing(self):
        r = self.client.patch(self.account_url, data=json.dumps({
            "emaaiill": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.account_url)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_update_user_account_incomplete_json(self):
        r = self.client.put(self.account_url, data=json.dumps({
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_complete_update_account(self):
        r = self.client.put(self.account_url, data=json.dumps({
            "username": "newusername",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "newusername")
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")
        self.assertEqual(r.data["email"], "newemail@newemail.com")
        self.assertEqual(r.data["location"], {"country": "", "city": "", "region": "", "street": ""})

    def test_complete_update_account_empty_json(self):
        r = self.client.put(self.account_url, data=json.dumps({
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "location": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        # Need five fields (mandatory)
        self.assertEqual(len(r.data), 4)

        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["email"], "test@test.com")
        self.assertEqual(r.data["location"], {"city": "", "region": "", "street": "", "country": ""})

    def test_change_password_not_logged_in(self):
        self.client.logout()

        r = self.client.put("%s%s/" % (self.account_url, "password"), data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

    def test_change_password(self):
        r = self.client.put("%s%s/" % (self.account_url, "password"), data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.login(password="password")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_change_password_with_false_old_password(self):
        r = self.client.put("%s%s/" % (self.account_url, "password"), data=json.dumps({
            "old_password": "passwor",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.get(self.logout_url)

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        r = self.login(password="password")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_change_password_empty_json(self):
        r = self.client.put("%s%s/" % (self.account_url, "password"), data=json.dumps({
            "old_password": "",
            "new_password": ""
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_partial_json(self):
        r = self.client.put("%s%s/" % (self.account_url, "password"), data=json.dumps({
            "old_password": "password"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_users_cant_have_same_username_update_patch(self):
        User.objects.create_user(username="username2", password="pass2")

        r = self.client.patch(self.account_url, data=json.dumps({
            "username": "username2",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

    def test_two_users_cant_have_same_username_update_put(self):
        User.objects.create_user(username="username2", password="pass2")

        r = self.client.put(self.account_url, data=json.dumps({
            "username": "username2",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com",
            "is_active": True,
            "location": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

    def test_can_put_account_with_same_username_without_conflict(self):
        r = self.client.put(self.account_url, data=json.dumps({
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com",
            "is_active": True,
            "location": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_can_patch_same_username_without_conflict(self):
        r = self.client.patch(self.account_url, data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_update_malformed_email_logged_in(self):
        r = self.client.patch(self.account_url, data=json.dumps({
            "email": "test",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_last_modification_date_on_update(self):
        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        datetime = r.data["last_modification_date"]

        self.client.patch(self.account_url, data=json.dumps({
            "email": "mail@mail.com",
        }), content_type="application/json")

        r = self.client.get(self.account_url)
        self.assertGreaterEqual(r.data["last_modification_date"], datetime)

    def test_405_when_get_on_password(self):
        r = self.client.get("%s%s/" % (self.account_url, "password"))
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_account_image(self):
        self.assertEqual(User.objects.get(pk=1).userprofile.image.name, "")

        r = self.post_image()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.client.get(self.account_url)
        self.assertNotEqual(r.data["profile_picture_url"], None)

    def test_post_account_image_already_existing_image(self):
        r = self.post_image()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(User.objects.get(pk=1).userprofile.image.name, "")

        r = self.post_image()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(User.objects.get(pk=1).userprofile.image.name, "")

    def test_patch_interested_by_categories(self):
        c1 = Category.objects.create(name="category1")
        c2 = Category.objects.create(name="category2")
        c3 = Category.objects.create(name="category3")

        r = self.patch_interested_by_categories([c1.id, c2.id, c3.id])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, [
            {"id": c1.id, "name": c1.name},
            {"id": c2.id, "name": c2.name},
            {"id": c3.id, "name": c3.name}
        ])

        r = self.patch_interested_by_categories([c2.id, c3.id])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, [
            {"id": c2.id, "name": c2.name},
            {"id": c3.id, "name": c3.name}
        ])

        r = self.patch_interested_by_categories([])
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, [])

    def test_get_pending_offers(self):
        c1 = Category.objects.create(name="Test")

        other_user = User.objects.create_user(username="user1", email="test@test.com",
                                              password="password")

        i1 = Item.objects.create(name="test1", description="test", price_min=50, price_max=60, owner=self.user,
                                 category=c1)
        i2 = Item.objects.create(name="test2", description="test", price_min=50, price_max=60, owner=other_user,
                                 category=c1)
        i3 = Item.objects.create(name="test3", description="test", price_min=50, price_max=60, owner=other_user,
                                 category=c1)
        i4 = Item.objects.create(name="test4", description="test", price_min=50, price_max=60, owner=other_user,
                                 category=c1)
        i5 = Item.objects.create(name="test4", description="test", price_min=50, price_max=60, owner=other_user,
                                 category=c1)

        now = timezone.now()

        o1 = Offer.objects.create(comment="test", item_given=i1, item_received=i2,
                                  creation_date=now + timezone.timedelta(seconds=4))
        o2 = Offer.objects.create(comment="test", item_given=i1, item_received=i3,
                                  creation_date=now + timezone.timedelta(seconds=3))
        Offer.objects.create(answered=True, comment="test", item_given=i4, item_received=i1)
        o4 = Offer.objects.create(comment="test", item_given=i5, item_received=i1,
                                  creation_date=now + timezone.timedelta(seconds=1))

        r = self.client.get(self.account_url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["pending_offers"]), 3)
        self.assertEqual(r.data["pending_offers"][0]["id"], o1.id)
        self.assertEqual(r.data["pending_offers"][1]["id"], o2.id)
        self.assertEqual(r.data["pending_offers"][2]["id"], o4.id)


class CSRFTests(TestCase):
    client = Client(enforce_csrf_checks=True)

    def test_get_and_set_csrf_(self):
        self.client.get("/api/csrf/")
        self.assertIn("csrftoken", self.client.cookies)


class LocationCoordinatesTests(TestCase):
    account_url = "/api/account/"

    new_location = {
        "street": "Route de Cheseaux 1",
        "city": "Yverdon-les-Bains",
        "region": "VD",
        "country": "Switzerland",
    }

    def put_location(self):
        return self.client.patch("%s%s/" % (self.account_url, "location"),
                                 data=json.dumps(self.new_location),
                                 content_type="application/json")

    def get_location(self):
        return User.objects.get_by_natural_key(self.user.username).location

    def get_coordinates(self):
        return User.objects.get_by_natural_key(self.user.username).coordinates

    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")

        self.patcher = patch("users.views.get_coordinates")
        self.get_coordinates_mock = self.patcher.start()
        self.get_coordinates_mock.return_value = [{"lat": 46.7793801, "lng": 6.659497600000001}]

    def tearDown(self):
        self.patcher.stop()

    def test_change_location_not_logged_in(self):
        self.client.logout()
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_location(self):
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get(self.account_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["location"], self.new_location)

    def test_change_location_empty_json(self):
        r = self.client.put("%s%s/" % (self.account_url, "location"), data=json.dumps({
            "location": {}
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_location_empty_json_fields(self):
        r = self.client.put("%s%s/" % (self.account_url, "location"), data=json.dumps({
            "location": {
                "street": "",
                "city": "",
                "region": "",
                "country": ""
            }
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_location_over_query_limit(self):
        self.get_coordinates_mock.side_effect = raise_over_query_limit_error
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coordinates_0_at_beginning(self):
        c = self.get_coordinates()
        self.assertEqual(c.latitude, 0)
        self.assertEqual(c.longitude, 0)

    def test_coordinates_and_location_do_not_change_after_zero_results_location_modification(self):
        self.get_coordinates_mock.return_value = []

        r = self.client.patch("%s%s/" % (self.account_url, "location"), data=json.dumps({
            "street": "fnupinom",
            "city": "fnupinom",
            "region": "fnupinom",
            "country": "fnupinom",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        c = self.get_coordinates()
        self.assertEqual(c.latitude, 0)
        self.assertEqual(c.longitude, 0)

        l = self.get_location()
        self.assertNotEqual(l.street, "fnupinom")
        self.assertNotEqual(l.city, "fnupinom")
        self.assertNotEqual(l.region, "fnupinom")
        self.assertNotEqual(l.country, "fnupinom")

    def test_coordinates_change_after_valid_location_modification(self):
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        c = self.get_coordinates()
        self.assertNotEqual(c.latitude, 0)
        self.assertNotEqual(c.longitude, 0)


class PublicAccountInfoTests(TestCase):
    users_url = "/api/users/"

    def post_item_image(self, image_name="test.png", item_id=1):
        with open("%s/%s" % (settings.MEDIA_TEST, image_name), "rb") as data:
            return self.client.post("/api/items/%d/images/" % item_id, {"image": data}, format="multipart")

    def post_user_image(self, image_name="test.png"):
        with open("%s/%s" % (settings.MEDIA_TEST, image_name), "rb") as data:
            return self.client.post("/api/account/image/", {"image": data}, format="multipart")

    def setUp(self):
        self.user = User.objects.create_user(username="username", first_name="first_name", last_name="last_name",
                                             email="test@test.com", password="password")

        self.c1 = Category.objects.create(name="category1")
        self.c2 = Category.objects.create(name="category2")
        self.c3 = Category.objects.create(name="category3")
        self.c4 = Category.objects.create(name="category4")
        self.c5 = Category.objects.create(name="category5")

        self.item = Item.objects.create(name="test", description="test", price_min=50, price_max=60,
                                        creation_date=timezone.now(), archived=False, owner=self.user, category=self.c1)

        self.user.location.city = "a"
        self.user.location.region = "b"
        self.user.location.country = "c"
        self.user.location.save()

        self.user.userprofile.categories.add(self.c1)
        self.user.userprofile.categories.add(self.c2)
        self.user.userprofile.categories.add(self.c3)
        self.user.userprofile.save()

        self.user.coordinates.latitude = 4
        self.user.coordinates.longitude = 4
        self.user.coordinates.save()

        self.client.login(username="username", password="password")
        self.post_user_image()
        self.client.logout()

    def test_get_user_info_not_found(self):
        r = self.client.get("%s%s%s/" % (self.users_url, self.user.username, "42"))
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_info(self):
        r = self.client.get("%s%s/" % (self.users_url, self.user.username))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], 1)
        self.assertIsNotNone(r.data["profile_picture_url"])
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["location"], "a, b, c")
        self.assertEqual(r.data["notes"], 0)
        self.assertEqual(r.data["note_avg"], None)
        self.assertEqual(r.data["interested_by"], [
            {"id": self.c1.id, "name": self.c1.name},
            {"id": self.c2.id, "name": self.c2.name},
            {"id": self.c3.id, "name": self.c3.name}
        ])
        self.assertEqual(r.data["coordinates"], {"latitude": 4, "longitude": 4})

        self.assertEqual(len(r.data["items"]), 1)
        item_received = r.data["items"][0]
        self.assertEqual(item_received["id"], 1)
        self.assertEqual(item_received["image_id"], None)
        self.assertEqual(item_received["image_url"], None)
        self.assertEqual(item_received["name"], "test")
        self.assertEqual(item_received["archived"], False)

    def test_get_inventory_item_images(self):
        self.client.login(username="username", password="password")
        self.post_item_image()
        self.client.logout()

        r = self.client.get("%s%s/" % (self.users_url, self.user.username))
        self.assertNotEqual(r.data["items"][0]["image_id"], None)
        self.assertNotEqual(r.data["items"][0]["image_url"], None)


class NoteAPITests(TestCase):
    notes_url = "/api/notes/"
    account_url = "/api/account/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        c1 = Category.objects.create(name="Test")

        self.other_user = User.objects.create_user(username="user1", email="test@test.com",
                                                   password="password")

        self.myItem = self.create_item(c1, self.current_user, name="Shoes", description="My old shoes", price_min=10,
                                       price_max=30)
        self.hisItem = self.create_item(c1, self.other_user, name="Shirt", description="My old shirt", price_min=5,
                                        price_max=30)
        Offer.objects.create(accepted=1, answered=True, comment="test", item_given=self.myItem,
                             item_received=self.hisItem)
        Offer.objects.create(accepted=0, answered=True, comment="test", item_given=self.myItem,
                             item_received=self.hisItem)

    def login(self):
        self.client.login(username="username", password="password")

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def post_note(self, offer=1, text="Test", note=0):
        return self.client.post(self.notes_url, data=json.dumps({
            "offer": offer,
            "text": text,
            "note": note
        }), content_type="application/json")

    def get_note(self, id_note):
        return self.client.get("%s%d/" % (self.notes_url, id_note), content_type="application/json")

    def delete_note(self, id_note):
        return self.client.delete("%s%d/" % (self.notes_url, id_note), content_type="application/json")

    def put_note(self, id_note, text="Test", note=0):
        return self.client.put("%s%d/" % (self.notes_url, id_note), data=json.dumps({
            "text": text,
            "note": note
        }), content_type="application/json")

    def patch_note(self, id_note, text="Test", note=0):
        return self.client.patch("%s%d/" % (self.notes_url, id_note), data=json.dumps({
            "text": text,
            "note": note
        }), content_type="application/json")

    def test_post_note(self):
        self.login()
        r = self.post_note(1, "test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_get_note(self):
        self.login()
        r = self.get_note(1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.get_note(1)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["user"], 2)
        self.assertEqual(r.data["offer"], 1)
        self.assertEqual(r.data["note"], 1)
        self.assertEqual(r.data["text"], "Test")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_post_note_under_0(self):
        self.login()
        r = self.post_note(1, "Test", -1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.logout()
        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 0)

    def test_post_note_over_5(self):
        self.login()
        r = self.post_note(1, "Test", 6)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.logout()
        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 0)

    def test_post_two_times_the_same_note(self):
        self.login()
        r = self.post_note(1, "Test", 1)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.logout()
        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 1)

    def test_put_note(self):
        self.login()
        r = self.put_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.put_note(1, "Test2", 2)
        self.assertEqual(r.data["note"], 2)
        self.assertEqual(r.data["text"], "Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_patch_note(self):
        self.login()
        r = self.patch_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.patch_note(1, "Test2", 2)
        self.assertEqual(r.data["note"], 2)
        self.assertEqual(r.data["text"], "Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_post_note_should_be_refused_if_offer_is_not_accepted(self):
        self.login()
        r = self.post_note(2, "test", 1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.logout()
        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 0)

    def test_user_avg_note_no_note(self):
        self.login()
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 0)
        self.assertEqual(r.data["note_avg"], None)

    def test_user_avg_note_one_note(self):
        self.login()
        self.post_note(1, "test", 1)
        r = self.client.get(self.account_url)
        self.client.logout()

        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 1)
        self.assertEqual(r.data["note_avg"], 1)

    def test_user_avg_note_two_notes(self):
        Offer.objects.create(accepted=1, answered=True, comment="test", item_given=self.myItem,
                             item_received=self.hisItem)

        self.login()
        self.post_note(1, "test", 2)
        self.post_note(3, "test", 3)
        self.client.logout()

        self.client.login(username="user1", password="password")
        r = self.client.get(self.account_url)
        self.assertEqual(r.data["notes"], 2)
        self.assertEqual(r.data["note_avg"], 2.5)


class ConsultationTests(TestCase):
    items_url = "/api/items/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.save()

        c = Category.objects.create(name="Test")
        Item.objects.create(name="Test", description="Test", price_min=1, price_max=2, archived=False, category=c,
                            owner=self.current_user)

    def login(self):
        self.client.login(username="username", password="password")

    def get_item(self, id_item=1):
        return self.client.get("%s%d/" % (self.items_url, id_item), content_type="application/json")

    def test_not_logged_user_consultation_should_do_nothing(self):
        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Consultation.objects.all()), 0)

    def test_logged_user_consultation_should_add_consultation(self):
        self.login()
        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Consultation.objects.all()), 1)
