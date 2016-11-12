import json

from django.test import Client, TestCase

from users.models import *


class UserProfileTests(TestCase):
    def test_user_profile_creation_after_user_creation(self):
        User.objects.create_user("username", "test@test.com", "password")
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_no_user_profile_creation_after_user_edit(self):
        User.objects.create_user("username", "test@test.com", "password")
        u = User.objects.get(pk=1)
        u.username = "username2"
        u.save()
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_deletion_on_user_deletion(self):
        User.objects.create_user("username", "test@test.com", "password")
        User.objects.get(pk=1).delete()
        self.assertEqual(UserProfile.objects.count(), 0)


class AccountAPITests(TestCase):
    c = Client()

    def post_user(self):
        return self.c.post("/api/users/", data=json.dumps({
            "username": "username",
            "email": "test@test.com",
            "password": "password"
        }), content_type="application/json")

    def login(self):
        return self.c.post("/api/login/", data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")

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

    def test_get_protected_user_info_not_logged_in(self):
        url = self.post_user()["Location"]
        r = self.c.get(url)
        self.assertEqual(r.status_code, 403)

    def test_get_protected_user_info_logged_in(self):
        url = self.post_user()["Location"]
        self.login()
        r = self.c.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["email"], "test@test.com")
        self.assertListEqual(r.data["categories"], [])
        self.assertEqual(r.data["account_active"], False)

    def test_change_password_not_logged_in(self):
        url = self.post_user()["Location"]
        r = self.c.patch(url, data=json.dumps({
            "password": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 403)

    def test_change_password_logged_in(self):
        url = self.post_user()["Location"]
        self.login()
        r = self.c.patch(url, data=json.dumps({
            "password": "test"
        }), content_type="application/json")
        self.assertEqual(r.status_code, 200)

    def test_logout(self):
        self.post_user()

        r = self.c.get("/api/logout/")
        self.assertEqual(r.status_code, 302)

        self.login()

        r = self.c.get("/api/logout/")
        self.assertEqual(r.status_code, 200)
