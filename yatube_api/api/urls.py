from django.urls import path, include
from rest_framework import routers

from api.views import PostViewSet, GroupViewsSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewsSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(
    r'posts/(?P<id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
]
