import json

import time
from django.test import Client, TestCase

from items.models import Category, Item, Like
from users.models import *


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


class AccountAPITests(TestCase):
    def post_user(self, username="username", first_name="first_name", last_name="last_name", email="test@test.com",
                  password="password"):
        return self.client.post("/api/users/", data=json.dumps({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }), content_type="application/json")

    def login(self, username="username", password="password"):
        return self.client.post("/api/login/", data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json")

    def test_user_creation(self):
        r = self.post_user()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r["Location"], "/api/users/1/")

    def test_user_creation_conflict(self):
        self.post_user()
        r = self.post_user()
        self.assertEqual(r.status_code, 409)

    def test_user_creation_incomplete_json(self):
        r = self.client.post("/api/users/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_user_creation_empty_json(self):
        r = self.post_user(username="", first_name="", last_name="", email="", password="")
        self.assertEqual(r.status_code, 400)

    def test_login_incorrect(self):
        self.post_user()
        r = self.login(username="username", password="passwor")
        self.assertEqual(r.status_code, 401)

    def test_login_incomplete_json(self):
        self.post_user()
        r = self.client.post("/api/login/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_login_emtpy_json(self):
        self.post_user()
        r = self.login(username="", password="")
        self.assertEqual(r.status_code, 400)

    def test_login_success(self):
        self.post_user()
        r = self.login()
        self.assertEqual(r.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_not_logged_in(self):
        self.post_user()

        r = self.client.get("/api/logout/")
        self.assertEqual(r.status_code, 401)

    def test_logout_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.get("/api/logout/")
        self.assertEqual(r.status_code, 200)

    def test_get_account_info_not_logged_in(self):
        self.post_user()
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 401)

    def test_get_account_info_logged_in(self):
        self.post_user()
        self.login()

        # add some data related to user
        u = User.objects.get(pk=1)
        c = Category.objects.create(name="category")
        u.userprofile.categories.add(c)
        i = Item.objects.create(name="test", description="test", price_min=50, price_max=60,
                                creation_date=timezone.now(), archived=False, owner=u.userprofile, category=c)
        Note.objects.create(user=u.userprofile, text="test", note=4)
        Like.objects.create(user=u.userprofile, item=i)

        r = self.client.get("/api/account/")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["id"], 1)
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
        self.assertListEqual(r.data["categories"], [1])
        self.assertListEqual(r.data["items"], [1])
        self.assertListEqual(r.data["notes"], [1])
        self.assertListEqual(r.data["likes"], [1])

    def test_update_account_not_logged_in(self):
        self.post_user()

        r = self.client.patch("/api/account/", data=json.dumps({
            "first_name": "f",
            "last_name": "l"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")

    def test_update_account_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "first_name": "firstname",
            "last_name": "lastname"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")

    def test_cannot_update_account_not_logged_in(self):
        self.post_user()

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "a@b.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.data["email"], "a@b.com")

    def test_cannot_connect_if_account_not_active(self):
        self.post_user()

        u = User.objects.get(pk=1)
        u.is_active = False
        u.save()

        r = self.client.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

        self.assertEqual(r.status_code, 401)

    def test_update_account_empty_json(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "username": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")

    def test_update_one_not_considered_info(self):
        self.post_user()
        self.login()
        datetime = str(timezone.now())

        r = self.client.patch("/api/account/", data=json.dumps({
            "last_modification_date": datetime,
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.data["last_modification_date"], datetime)

    def test_update_account_malformed_json(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "emaaiill": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_update_user_account_incomplete_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/", data=json.dumps({
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 3)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_complete_update_account(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/", data=json.dumps({
            "username": "newusername",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "newusername")
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")
        self.assertEqual(r.data["email"], "newemail@newemail.com")
        self.assertEqual(r.data["location"], {'country': '', 'city': '', 'region': '', 'street': ''})

    def test_complete_update_account_empty_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/", data=json.dumps({
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "location": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        # Need five fields (mandatory)
        self.assertEqual(len(r.data), 4)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["email"], "test@test.com")
        self.assertEqual(r.data["location"], {'city': '', 'region': '', 'street': '', 'country': ''})

    def test_change_password_not_logged_in(self):
        self.post_user()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

    def test_change_password(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)

        r = self.login(password="password")
        self.assertEqual(r.status_code, 401)

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, 200)

    def test_change_password_with_false_old_password(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "passwor",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

        self.client.get("/api/account/logout/")

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, 401)

        r = self.login(password="password")
        self.assertEqual(r.status_code, 200)

    def test_change_password_empty_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "",
            "new_password": ""
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_change_password_partial_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "password"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    # FIXME atomic errors
    """def test_two_users_cant_have_same_username_update_patch(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.client.patch("/api/account/", data=json.dumps({
            "username": "user2",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 409)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user1")

        self.client.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user2")

    def test_two_users_cant_have_same_username_update_put(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.client.put("/api/account/", data=json.dumps({
            "username": "user2",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com",
            "is_active": True,
            "location": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 409)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user1")

        self.client.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user2")"""

    def test_update_malformed_email_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "test",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_modification_date_user_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        datetime = r.data["last_modification_date"]

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "mail@mail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "mail@mail.com")
        time.sleep(0.2)
        self.assertGreaterEqual(r.data["last_modification_date"], datetime)

    def test_405_when_get_on_password(self):
        self.post_user()
        self.login()
        r = self.client.get("/api/account/password/")
        self.assertEqual(r.status_code, 405)


class CSRFTests(TestCase):
    client = Client(enforce_csrf_checks=True)

    def test_get_and_set_csrf_(self):
        self.client.get("/api/csrf/")
        self.assertIn("csrftoken", self.client.cookies)


class LocationCoordinatesTests(TestCase):

    new_location = {
        "street": "Route de Cheseaux 1",
        "city": "Yverdon-les-Bains",
        "region": "VD",
        "country": "Switzerland",
    }

    def put_location(self):
        return self.client.patch("/api/account/location/",
                                 data=json.dumps(self.new_location),
                                 content_type="application/json")

    def get_coordinates(self):
        return User.objects.get_by_natural_key(self.user.username).coordinates

    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")

    def test_change_location_not_logged_in(self):
        self.client.logout()
        r = self.put_location()
        self.assertEqual(r.status_code, 401)

    def test_change_location(self):
        r = self.put_location()
        self.assertEqual(r.status_code, 200)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["location"], self.new_location)

    def test_change_location_empty_json(self):
        r = self.client.put("/api/account/location/", data=json.dumps({
            "location": {}
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_change_location_empty_json_fields(self):
        r = self.client.put("/api/account/location/", data=json.dumps({
            "location": {
                "street": "",
                "city": "",
                "region": "",
                "country": ""
            }
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_coordinates_0_at_beginning(self):
        c = self.get_coordinates()
        self.assertEqual(c.latitude, 0)
        self.assertEqual(c.longitude, 0)

    def test_coordinates_do_not_change_after_zero_results_location_modification(self):
        r = self.client.patch("/api/account/location/", data=json.dumps({
            "street": "fnupinom",
            "city": "fnupinom",
            "region": "fnupinom",
            "country": "fnupinom",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

        c = self.get_coordinates()
        self.assertEqual(c.latitude, 0)
        self.assertEqual(c.longitude, 0)

    def test_coordinates_change_after_valid_location_modification(self):
        r = self.put_location()
        self.assertEqual(r.status_code, 200)

        c = self.get_coordinates()
        self.assertNotEqual(c.latitude, 0)
        self.assertNotEqual(c.longitude, 0)


class PublicAccountInfoTests(TestCase):
    def test_get_user_info(self):
        u = User.objects.create_user(username="username", first_name="first_name", last_name="last_name",
                                     email="test@test.com", password="password")
        u.location.city = "a"
        u.location.region = "b"
        u.location.country = "c"
        u.location.save()

        r = self.client.get("/api/users/%s/" % (u.username + "42"))
        self.assertEquals(r.status_code, 404)

        r = self.client.get("/api/users/%s/" % u.username)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["location"], "a, b, c")
        self.assertListEqual(r.data["items"], [])
        self.assertListEqual(r.data["notes"], [])
        self.assertListEqual(r.data["likes"], [])
