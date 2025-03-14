from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from post.models import Post, UserPostRelation


class PostSerializer(ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'header', 'description', 'likes', 'rating')


class UserPostRelationSerializer(ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = ('post', 'is_like', 'is_bookmark')

    def update(self, instance, validated_data):
        """Пересчет лайков при обновлении"""
        response = super().update(instance, validated_data)
        instance.post.update_likes()
        return response