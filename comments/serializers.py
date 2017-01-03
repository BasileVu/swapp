from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('content', 'date', 'user', 'item')

# FIXME : DELETE CommentItemSerializer


class CommentItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'date')
