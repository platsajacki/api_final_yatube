from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAdminUser, IsAuthenticated, SAFE_METHODS
)

from .pagination import PostPaginator
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from posts.models import Post, Group, Follow, User


class UpdateDestroyMixin:
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'У вас недостаточно прав для выполнения данного действия.'
            )
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'У вас недостаточно прав для выполнения данного действия.'
            )
        super().perform_destroy(instance)


class PostViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    pagination_class = PostPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['idFollow'])

    def get_queryset(self):
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewsSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return (IsAdminUser(),)
        return super().get_permissions()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']
    filter_backends = (SearchFilter,)
    search_fields = ('following',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def get_following(self):
        return get_object_or_404(
            User, username=self.request.data.get('following')
        )

    def perform_create(self, serializer):
        if (
            (following := self.get_following()) == self.request.user
            or self.get_queryset().filter(following=following).exists()
        ):
            raise ValidationError('Неверный запрос на подписку.')
        serializer.save(user=self.request.user, following=following)
