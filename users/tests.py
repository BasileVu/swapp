import json
import time

from django.test import Client, TestCase
from rest_framework import status

from items.models import *
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
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r["Location"], "/api/users/1/")

    def test_user_creation_conflict(self):
        self.post_user()
        r = self.post_user()
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

    def test_user_creation_incomplete_json(self):
        r = self.client.post("/api/users/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_empty_json(self):
        r = self.post_user(username="", first_name="", last_name="", email="", password="")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_incorrect(self):
        self.post_user()
        r = self.login(username="username", password="passwor")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_incomplete_json(self):
        self.post_user()
        r = self.client.post("/api/login/", data=json.dumps({
            "username": "username"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_emtpy_json(self):
        self.post_user()
        r = self.login(username="", password="")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        self.post_user()
        r = self.login()
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_not_logged_in(self):
        self.post_user()

        r = self.client.get("/api/logout/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.get("/api/logout/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_get_account_info_not_logged_in(self):
        self.post_user()
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account_info_logged_in(self):
        self.post_user()
        self.login()

        # add some data related to user
        u = User.objects.get(pk=1)
        c = Category.objects.create(name="category")
        u.userprofile.categories.add(c)
        i = Item.objects.create(name="test", description="test", price_min=50, price_max=60,
                                creation_date=timezone.now(), archived=False, owner=u, category=c)
        o = Offer.objects.create(accepted=True, status=True, item_given=i, item_received=i)
        Note.objects.create(user=u, offer=o, text="test", note=4)
        Like.objects.create(user=u, item=i)

        r = self.client.get("/api/account/")

        self.assertEqual(r.status_code, status.HTTP_200_OK)
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
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")

    def test_update_account_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "first_name": "firstname",
            "last_name": "lastname"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["first_name"], "firstname")
        self.assertEqual(r.data["last_name"], "lastname")

    def test_cannot_update_account_not_logged_in(self):
        self.post_user()

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "a@b.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        self.login()

        # Test if no modification
        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_account_empty_json(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "username": "",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "username")

    def test_update_one_not_considered_info(self):
        self.post_user()
        self.login()
        datetime = str(timezone.now())

        r = self.client.patch("/api/account/", data=json.dumps({
            "last_modification_date": datetime,
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertNotEqual(r.data["last_modification_date"], datetime)

    def test_update_account_malformed_json(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "emaaiill": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_update_user_account_incomplete_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/", data=json.dumps({
            "email": "newemail@newemail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 3)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        # Need five fields (mandatory)
        self.assertEqual(len(r.data), 4)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

    def test_change_password(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "password",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.login(password="password")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_change_password_with_false_old_password(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "passwor",
            "new_password": "newpassword"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.get("/api/account/logout/")

        r = self.login(password="newpassword")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

        r = self.login(password="password")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_change_password_empty_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "",
            "new_password": ""
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_partial_json(self):
        self.post_user()
        self.login()

        r = self.client.put("/api/account/password/", data=json.dumps({
            "old_password": "password"
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # FIXME atomic errors
    """def test_two_users_cant_have_same_username_update_patch(self):
        self.post_user(username="user1", password="pass1")
        self.post_user(username="user2", password="pass2")
        self.login(username="user1", password="pass1")

        r = self.client.patch("/api/account/", data=json.dumps({
            "username": "user2",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "user1")

        self.client.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "user1")

        self.client.get("/api/logout/")
        self.login(username="user2", password="pass2")

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["username"], "user2")"""

    def test_update_malformed_email_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "test",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 1)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["email"], "test@test.com")

    def test_modification_date_user_logged_in(self):
        self.post_user()
        self.login()

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        datetime = r.data["last_modification_date"]

        r = self.client.patch("/api/account/", data=json.dumps({
            "email": "mail@mail.com",
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual("password" in r.data, False)
        self.assertEqual(len(r.data), 0)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
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

    def get_location(self):
        return User.objects.get_by_natural_key(self.user.username).location

    def get_coordinates(self):
        return User.objects.get_by_natural_key(self.user.username).coordinates

    def setUp(self):
        self.user = User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")

    def test_change_location_not_logged_in(self):
        self.client.logout()
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_location(self):
        r = self.put_location()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = self.client.get("/api/account/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["location"], self.new_location)

    def test_change_location_empty_json(self):
        r = self.client.put("/api/account/location/", data=json.dumps({
            "location": {}
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_location_empty_json_fields(self):
        r = self.client.put("/api/account/location/", data=json.dumps({
            "location": {
                "street": "",
                "city": "",
                "region": "",
                "country": ""
            }
        }), content_type="application/json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_coordinates_0_at_beginning(self):
        c = self.get_coordinates()
        self.assertEqual(c.latitude, 0)
        self.assertEqual(c.longitude, 0)

    def test_coordinates_and_location_do_not_change_after_zero_results_location_modification(self):
        r = self.client.patch("/api/account/location/", data=json.dumps({
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
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["first_name"], "first_name")
        self.assertEqual(r.data["last_name"], "last_name")
        self.assertEqual(r.data["username"], "username")
        self.assertEqual(r.data["location"], "a, b, c")
        self.assertListEqual(r.data["items"], [])
        self.assertListEqual(r.data["notes"], [])
        self.assertListEqual(r.data["likes"], [])


class NoteAPITests(TestCase):
    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.location = "location"
        self.current_user.userprofile.save()

        c1 = Category.objects.create(name="Test")

        self.other_user = User.objects.create_user(username="user1", email="test@test.com",
                                                   password="password")

        self.myItem = self.create_item(c1, self.current_user, name="Shoes", description="My old shoes", price_min=10, price_max=30)
        self.hisItem = self.create_item(c1, self.other_user, name="Shirt", description="My old shirt", price_min=5,
                                        price_max=30)
        Offer.objects.create(id=1, accepted=1, status=1, comment="test", item_given=self.myItem, item_received=self.hisItem)
        Offer.objects.create(id=2, accepted=0, status=1, comment="test", item_given=self.myItem,
                                          item_received=self.hisItem);

    def login(self):
        self.client.login(username="username", password="password")

    def create_item(self, category, owner, name="Test", description="Test", price_min=1, price_max=2, archived=0):
        return Item.objects.create(name=name, description=description, price_min=price_min, price_max=price_max,
                                   archived=archived, category=category, owner=owner)

    def post_note(self, offer=1, text="Test", note=0):
        return self.client.post("/api/notes/", data=json.dumps({
            "offer": offer,
            "text": text,
            "note": note
        }), content_type="application/json")

    def get_notes(self):
        return self.client.get("/api/notes/", content_type="application/json")

    def get_note(self, id_note):
        return self.client.get("/api/notes/" + str(id_note) + "/", content_type="application/json")

    def delete_note(self, id_note):
        return self.client.delete("/api/notes/" + str(id_note) + "/", content_type="application/json")

    def put_note(self, id_note, text="Test", note=0):
        return self.client.put("/api/notes/" + str(id_note) + "/", data=json.dumps({
            "text": text,
            "note": note
        }), content_type="application/json")

    def patch_note(self, id_note, text="Test", note=0):
        return self.client.patch("/api/notes/" + str(id_note) + "/", data=json.dumps({
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
        self.assertEqual(r.status_code, 404)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.get_note(1)
        self.assertEqual(r.data["id"], 1)
        self.assertEqual(r.data["user"], 2)
        self.assertEqual(r.data["offer"], 1)
        self.assertEqual(r.data["note"], 1)
        self.assertEqual(r.data["text"], "Test")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_get_notes(self):
        self.login()
        r = self.get_notes()
        self.assertEqual(len(r.data), 0)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.get_notes()
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["id"], 1)
        self.assertEqual(r.data[0]["user"], 2)
        self.assertEqual(r.data[0]["offer"], 1)
        self.assertEqual(r.data[0]["note"], 1)
        self.assertEqual(r.data[0]["text"], "Test")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_post_note_under_0(self):
        self.login()
        r = self.post_note(1, "Test", -1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_note_over_5(self):
        self.login()
        r = self.post_note(1, "Test", 6)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_two_times_the_same_note(self):
        self.login()
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note(self):
        self.login()
        r = self.put_note(1, "Test", 1)
        self.assertEqual(r.status_code, 404)
        r = self.post_note(1, "Test", 1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.put_note(1, "Test2", 2)
        self.assertEqual(r.data["note"], 2)
        self.assertEqual(r.data["text"], "Test2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_patch_note(self):
        self.login()
        r = self.patch_note(1, "Test", 1)
        self.assertEqual(r.status_code, 404)
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


class ConsultationTests(TestCase):
    url = "/api/items/"

    def setUp(self):
        self.current_user = User.objects.create_user(username="username", email="test@test.com", password="password")
        self.current_user.userprofile.save()

        c = Category.objects.create(name="Test")
        Item.objects.create(name="Test", description="Test", price_min=1, price_max=2, archived=False, category=c,
                            owner=self.current_user)

    def login(self):
        self.client.login(username="username", password="password")

    def get_item(self, id_item=1):
        return self.client.get(self.url + str(id_item) + "/", content_type="application/json")

    def test_not_logged_user_consultation_should_do_nothing(self):

        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Consultation.objects.all()), 0)

    def test_logged_user_consultation_should_add_consultation(self):
        self.login()
        r = self.get_item()
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Consultation.objects.all()), 1)
        consultation = Consultation.objects.first()