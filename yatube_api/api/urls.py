from django.urls import path
from api.views import CommentViewSet, GroupViewSet, PostViewSet
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='posts')
router.register('groups', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
