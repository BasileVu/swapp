from django.test import TestCase

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
