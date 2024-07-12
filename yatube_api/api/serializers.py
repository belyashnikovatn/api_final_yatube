from rest_framework.validators import UniqueTogetherValidator
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
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def create(self, validated_data):
        if validated_data['following'] == validated_data['user']:
            raise serializers.ValidationError(
                'Нельзя оформить подписку на себя!')

        return Follow.objects.create(**validated_data)
