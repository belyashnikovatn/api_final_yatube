from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created', 'post')
        read_only_fields = ('post',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializator(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    # following = serializers.StringRelatedField(
    #     read_only=True
    # )
    user = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Follow
        # fields = ('id', 'user', 'following')
        fields = '__all__'
