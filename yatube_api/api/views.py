from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, get_list_or_404

from posts.models import Group, Post, Follow

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import filters

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions


from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializator)


class PostViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    @property
    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        new_queryset = self.get_post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        super(CommentViewSet, self).perform_destroy(instance)


# class FollowViewSet(viewsets.ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializator
#     permission_classes = (permissions.IsAuthenticated,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username',)


class FollowCreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializator
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        # queryset = get_list_or_404(Follow, user=self.request.user)
        # queryset = self.filter_queryset(Follow, user=self.request.user)
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(following__username=username)
        # new_queryset = self.filter_queryset(Follow, user=self.request.user)
        # new_queryset = self.filter_queryset(Follow.objects.filter(user=self.request.user))
        return queryset

    # def create(self, validated_data):
    #     Follow.objects.create(following=validated_data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
