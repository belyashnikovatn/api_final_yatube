from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, FollowCreateListViewSet, GroupViewSet,
                       PostViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('posts', PostViewSet)
v1_router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='posts')
v1_router.register('groups', GroupViewSet)
v1_router.register(r'follow', FollowCreateListViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
