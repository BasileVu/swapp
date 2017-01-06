from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_fullname = serializers.SerializerMethodField()
    user_profile_picture = serializers.SerializerMethodField()

    def get_user_fullname(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)

    def get_user_profile_picture(self, obj):
        return None if obj.user.userprofile.image.name == "" else obj.user.userprofile.image.url

    class Meta:
        model = Comment
        fields = ("id", "content", "date", "user", "item", "user_fullname", "user_profile_picture")
