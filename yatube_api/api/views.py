from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import OwnerOnly, ReadOnly
from api.serializers import (CommentSerializer, FollowSerializator,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOnly, ReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOnly, ReadOnly)

    @property
    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class FollowCreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = FollowSerializator
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.following.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
