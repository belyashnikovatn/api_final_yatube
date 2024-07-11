from django.urls import path
from api.views import (
    CommentViewSet, GroupViewSet, PostViewSet, FollowCreateListViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='posts')
router.register('groups', GroupViewSet)
router.register(r'follow', FollowCreateListViewSet, basename='follow')

# router.register('follow', FollowViewSet)
# router.register(r'follow', FollowCreateListViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
