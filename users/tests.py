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
    c = Client()

    def post_user(self, username="username", email="test@test.com", password="password"):
        return self.c.post("/api/users/", data=json.dumps({
            "username": username,
            "email": email,
            "password": password
        }), content_type="application/json")

    def login(self, username="username", password="password"):
        return self.c.post("/api/login/", data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json")

    def create_elements_with_user_link(self, name="test", pk=1):
        u = User.objects.get(pk=pk)

        c = Category(name=name)
        c.save()
        u.userprofile.categories.add(c)

        i = Item(name="test", description="test", price_min=50, price_max=60, creation_date=timezone.now(),
                 archived=False, owner=u.userprofile, category=c)
        i.save()

        n = Note(user=u.userprofile, text="test", note=4)
        n.save()

        l = Like(user=u.userprofile, item=i)
        l.save()

    def test_user_creation(self):
        r = self.post_user()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r["Location"], "/api/users/1/")

    def test_user_creation_conflict(self):
        self.post_user()
        r = self.post_user()
        self.assertEqual(r.status_code, 409)

    def test_incomplete_json(self):
        r = self.c.post("/api/users/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_empty_json(self):
        r = self.post_user(username="", password="")
        self.assertEqual(r.status_code, 400)

    def test_login_incorrect(self):
        self.post_user()
        r = self.login(username="username", password="passwor")
        self.assertEqual(r.status_code, 401)

    def test_login_incomplete_json(self):
        self.post_user()
        r = self.c.post("/api/login/", data=json.dumps({
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

    def test_logout_not_logged_in(self):
        self.post_user()

        r = self.c.get("/api/logout/")
        self.assertEqual(r.status_code, 401)

    def test_logout_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.get("/api/logout/")
        self.assertEqual(r.status_code, 200)

    def test_get_account_info_not_logged_in(self):
        self.post_user()
        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 401)

    def test_get_account_info_logged_in(self):
        self.post_user()
        self.login()
        self.create_elements_with_user_link()

        r = self.c.get("/api/account/")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["first_name"], "")
        self.assertEqual(r.data["last_name"], "")
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

        r = self.c.patch("/api/account/", data=json.dumps({
            "first_name": "firstname",
            "last_name": "lastname"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "")
        self.assertEqual(r.data["last_name"], "")

    def test_update_account_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.patch("/api/account/", data=json.dumps({
            "first_name": "firstname",
            "last_name": "lastname"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")

    def test_cannot_update_account_not_logged_in(self):
        self.post_user()

        r = self.c.patch("/api/account/", data=json.dumps({
            "email": "a@b.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.data["email"], "a@b.com")

    def test_cannot_connect_if_account_not_active(self):
        self.post_user()

        u = User.objects.get(pk=1)
        u.is_active = False
        u.save()

        r = self.c.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

        self.assertEqual(r.status_code, 401)

    def test_update_account_empty_json(self):
        self.post_user()
        self.login()

        r = self.c.patch("/api/account/", data=json.dumps({
            "username": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")

    def test_update_one_not_considered_info(self):
        self.post_user()
        self.login()
        datetime = str(timezone.now())

        r = self.c.patch("/api/account/", data=json.dumps({
            "last_modification_date": datetime,
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.data["last_modification_date"], datetime)

    def test_update_account_malformed_json(self):
        self.post_user()
        self.login()

        r = self.c.patch("/api/account/", data=json.dumps({
            "emaaiill": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_update_user_account_incomplete_json(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/", data=json.dumps({
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        # Need 3 fields (mandatory)
        self.assertEqual(len(r.data), 3)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_complete_update_account(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/", data=json.dumps({
            "username": "newusername",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "newusername")
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")
        self.assertEqual(r.data["email"], "newemail@newemail.com")
        self.assertEqual(r.data["location"], {'country': '', 'city': '', 'region': '', 'street': ''})

    def test_complete_update_account_empty_json(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/", data=json.dumps({
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "location": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        # Need five fields (mandatory)
        self.assertEqual(len(r.data), 4)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["first_name"], "")
        self.assertEqual(r.data["last_name"], "")
        self.assertEqual(r.data["email"], "test@test.com")
        self.assertEqual(r.data["location"], {'city': '', 'region': '', 'street': '', 'country': ''})

    def test_change_password_not_logged_in(self):
        self.post_user()

        r = self.c.put("/api/account/password/", data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

    def test_change_password_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/password/", data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)

        r = self.login(password="password")
        self.assertEqual(r.status_code, 401)

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, 200)

    def test_change_password_with_false_old_password_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/password/", data=json.dumps({
            "old_password": "passwor",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

        self.c.get("/api/account/logout/")

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, 401)

        r = self.login(password="password")
        self.assertEqual(r.status_code, 200)

    def test_change_password_empty_json_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/password/", data=json.dumps({
            "old_password": "",
            "new_password": ""
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    # FIXME atomic errors
    """def test_two_users_cant_have_same_username_update_patch(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.c.patch("/api/account/", data=json.dumps({
            "username": "user2",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 409)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user1")

        self.c.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user2")

    def test_two_users_cant_have_same_username_update_put(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.c.put("/api/account/", data=json.dumps({
            "username": "user2",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com",
            "is_active": True,
            "location": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 409)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user1")

        self.c.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user2")"""

    def test_update_malformed_email_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.patch("/api/account/", data=json.dumps({
            "email": "test",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_modification_date_user_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        datetime = r.data["last_modification_date"]

        r = self.c.patch("/api/account/", data=json.dumps({
            "email": "mail@mail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "mail@mail.com")
        time.sleep(0.2)
        self.assertGreaterEqual(r.data["last_modification_date"], datetime)

    def test_change_location_not_logged_in(self):
        self.post_user()
        r = self.c.patch("/api/account/", data=json.dumps({
            "location": "location"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)

    def test_change_location_logged_in(self):
        self.post_user()
        self.login()

        location = {
            "street": "street",
            "city": "city",
            "country": "country",
            "region": "region"
        }

        r = self.c.put("/api/account/location/", data=json.dumps(location), content_type="application/json")
        self.assertEqual(r.status_code, 200)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["location"], location)

    def test_change_location_empty_json(self):
        self.post_user()
        self.login()
        r = self.c.put("/api/account/", data=json.dumps({
            "location": {}
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_405_when_get_on_password(self):
        self.post_user()
        self.login()
        r = self.c.get("/api/account/password/")
        self.assertEqual(r.status_code, 405)


class CSRFTests(TestCase):
    c = Client(enforce_csrf_checks=True)

    def get_csrf(self):
        return self.c.cookies.get("csrftoken").value

    def login(self, username="username", password="password", with_csrf=False):
        extra = {}
        if with_csrf:
            extra["HTTP_X_CSRFTOKEN"] = self.get_csrf()
        return self.c.post("/api/login/", data=json.dumps({
            "username": username,
            "password": password
        }), content_type="application/json", **extra)

    def post_user(self, username="username", email="email", password="password", with_csrf=False):
        extra = {}
        if with_csrf:
            extra["HTTP_X_CSRFTOKEN"] = self.get_csrf()
        return self.c.post("/api/users/", data=json.dumps({
            "username": username,
            "email": email,
            "password": password
        }), content_type="application/json", **extra)

    def setUp(self):
        self.c.get("/api/csrf/")

    def test_get_and_set_csrf_(self):
        self.assertIn("csrftoken", self.c.cookies)

    """
    # FIXME find why it works without csrf
    '''def test_register_without_csrf(self):
        r = self.post_user()
        self.assertEqual(r.status_code, 403)'''

    def test_register_with_csrf(self):
        r = self.post_user(with_csrf=True)
        self.assertEqual(r.status_code, 201)

    def test_login_without_csrf(self):
        self.post_user(with_csrf=True)
        r = self.login()
        self.assertEqual(r.status_code, 403)

    def test_login_with_csrf(self):
        self.post_user(with_csrf=True)
        r = self.login(with_csrf=True)
        self.assertEqual(r.status_code, 200)

    def test_change_email_without_csrf(self):
        self.post_user(with_csrf=True)
        self.login(with_csrf=True)
        r = self.c.put("/api/account/", data=json.dumps({  # FIXME
            "email": "t@t.com"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 403)

    def test_change_email_with_csrf(self):
        self.post_user(with_csrf=True)
        self.login(with_csrf=True)
        r = self.c.patch("/api/account/", data=json.dumps({  # FIXME
            "email": "t@t.com"
        }), content_type="application/json", HTTP_X_CSRFTOKEN=self.get_csrf())
        self.assertEqual(r.status_code, 200)"""


