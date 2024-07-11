from django.urls import path
from api.views import (
    CommentViewSet, GroupViewSet, PostViewSet, FollowCreateListViewSet,
    FollowViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='posts')
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)

# router.register(r'follow', FollowCreateListViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
