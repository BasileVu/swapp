from rest_framework import serializers

<<<<<<< HEAD
from items.models import Item, Category
from users.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(source="item_set", many=True, queryset=Item.objects.all())
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'account_active', 'items', 'categories')


class UserNameSerializer(serializers.ModelSerializer):
=======
from users.models import *


"""class UserAccountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.StringRelatedField()
    first_name = serializers.StringRelatedField()
    last_name = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    categories = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    account_active = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        # TODO add location field
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'account_active', 'last_modification_date',
            'categories', 'items', 'notes', 'likes'
        )

    def get_categories(self, obj):
        return obj.userprofile.categories.values_list('id', flat=True)

    def get_items(self, obj):
        return obj.userprofile.item_set.values_list('id', flat=True)

    def get_notes(self, obj):
        return obj.userprofile.note_set.values_list('id', flat=True)

    def get_likes(self, obj):
        return obj.userprofile.like_set.values_list("id", flat=True)

    def get_account_active(self, obj):
        return obj.userprofile.account_active"""


class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        # TODO add location field
        fields = (
            'username', 'first_name', 'last_name', 'email', 'account_active',
        )
        extra_kwargs = {'account_active': {'write_only': True}}


"""class UserNameSerializer(serializers.ModelSerializer):
>>>>>>> 00c6a9d... user-rest improvement
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
        fields = ('account_active',)"""


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
