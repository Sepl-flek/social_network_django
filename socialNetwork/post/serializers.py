from rest_framework.serializers import ModelSerializer

from post.models import Post, UserPostRelation


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserPostRelationSerializer(ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = ('post', 'is_like', 'is_bookmark')

    def update(self, instance, validated_data):
        """Пересчет лайков при обновлении"""
        response = super().update(instance, validated_data)
        instance.post.update_likes()
        return response