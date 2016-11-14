from rest_framework import serializers

from items.models import Item, Category
from users.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'account_active', 'items', 'categories')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserFirstNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)


class UserLastNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name',)


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileAccountActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('account_active',)


class UserProfileLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('location',)
        extra_kwargs = {'location': {'required': True}}


# A adapter
class UserProfileCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('categories',)


# A adapter
"""class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user.id", queryset=User.objects.all())

    class Meta:
        model = Note
        fields = ('id', 'user_id', 'text', 'note')"""
