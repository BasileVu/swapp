import json
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

        # test dates modification


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

    def test_login_incorrect(self):
        self.post_user()
        r = self.c.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "passwor"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)

    def test_login_incomplete_json(self):
        self.post_user()
        r = self.c.post("/api/login/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
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

    def test_get_protected_user_info_not_logged_in(self):
        self.post_user()
        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 401)

    def test_get_protected_user_info_logged_in(self):
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
        self.assertEqual(r.data["account_active"], False)
        self.assertNotEqual(r.data["last_modification_date"], "")
        self.assertListEqual(r.data["categories"], [1])
        self.assertListEqual(r.data["items"], [1])
        self.assertListEqual(r.data["notes"], [1])
        self.assertListEqual(r.data["likes"], [1])

        r = self.c.patch("/api/account/", data=json.dumps({
            "first_name": "firstname",
            "last_name": "lastname"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)

        r = self.c.get("/api/account/")

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")

    def test_update_user_info_not_logged_in(self):
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

    def test_update_user_info_logged_in(self):
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

    def test_update_one_user_info_not_logged_in(self):
        self.post_user()

        r = self.c.patch("/api/account/", data=json.dumps({
            "account_active": True,
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["account_active"], False)

    def test_update_one_user_info_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.patch("/api/account/", data=json.dumps({
            "account_active": True,
        }), content_type="application/json")
        print(json.dumps({
            "account_active": True,
        }))
        self.assertEqual(r.status_code, 200)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["account_active"], True)

    def test_update_one_not_considered_user_info_logged_in(self):
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

    def test_update_one_user_info_patch_malformed_json_logged_in(self):
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

    def test_update_one_user_info_put_malformed_json_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/", data=json.dumps({
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual("password" in r.data, False)
        # Need three more fields (mandatory)
        self.assertEqual(len(r.data), 3)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_complete_update_user_info_not_logged_in(self):
        self.post_user()

        r = self.c.put("/api/account/", data=json.dumps({
            "username": "newusername",
            "first_name": "firstname",
            "last_name": "last_name",
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 401)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["first_name"], "")
        self.assertEqual(r.data["last_name"], "")
        self.assertEqual(r.data["email"], "test@test.com")

    def test_complete_update_user_info_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.put("/api/account/", data=json.dumps({
            "username": "newusername",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "newemail@newemail.com",
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

    def test_two_users_cant_have_same_username_update(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.c.patch("/api/account/", data=json.dumps({
            "username": "user2",
        }), content_type="application/json")
        self.assertEqual(r.status_code, 404)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.c.get("/api/account/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "user1")

    """def test_change_email_not_logged_in(self):
        self.post_user()
        r = self.c.patch("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")
        r = self.patch_field_user("/api/account/email/", "email", "e@e.com")
        self.assertEqual(r.status_code, 401)

    def test_change_email_logged_in(self):
        self.post_user()
        self.login()
        r = self.patch_field_user("/api/account/email/", "email", "e@e.com")
        self.assertEqual(r.status_code, 200)

    def test_change_password_not_logged_in(self):
        self.post_user()
        r = self.patch_field_user("/api/account/email/", "password", "test")
        self.assertEqual(r.status_code, 401)

    def test_change_password_logged_in(self):
        self.post_user()
        self.login()
        r = self.patch_field_user("/api/account/email/", "password", "test")
        self.assertEqual(r.status_code, 200)"""

    """def test_get_username_not_logged_in(self):
        self.post_user()
        r = self.c.get("/api/account/username/")
        self.assertEqual(r.status_code, 401)

    def test_get_username_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.get("/api/account/username/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "username")

    def test_put_get_firstname(self):
        self.post_user()

        r = self.patch_field_user("/api/account/first_name/", "first_name", "firstname")
        self.assertEqual(r.status_code, 401)

        r = self.c.get("/api/account/first_name/")
        self.assertEqual(r.status_code, 401)

        self.login()

        r = self.c.get("/api/account/first_name/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "")

        r = self.patch_field_user("/api/account/first_name/", "first_name", "firstname")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "firstname")"""

    """def test_put_get_firstname_logged_in(self):
        url = self.post_user()["Location"] + "first_name/"
        self.login()

        r = self.put_field_user(url, "first_name", "firstname")
        self.assertEqual(r.status_code, 200)

        r = self.c.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["first_name"], "username")"""

    """def test_get_email_not_logged_in(self):
        self.post_user()
        r = self.c.get("/api/account/email/")
        self.assertEqual(r.status_code, 401)

    def test_get_email_logged_in(self):
        self.post_user()
        self.login()

        r = self.c.get("/api/account/email/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["email"], "test@test.com")"""
