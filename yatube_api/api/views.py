from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Follow, Group, Post, User


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
    serializer_class = PostSerializer

    def get_queryset(self):
        if (
            'limit' in self.request.query_params
            and 'offset' in self.request.query_params
        ):
            self.pagination_class = LimitOffsetPagination
        return Post.objects.select_related('author', 'group')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['id'])

    def get_queryset(self):
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewsSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            following = User.objects.get(
                username=self.request.data.get('following')
            )
        except Exception:
            raise ValidationError('Такого пользователя не существует.')
        if (
            following == self.request.user
            or self.get_queryset().filter(following=following).exists()
        ):
            raise ValidationError('Неверный запрос на подписку.')
        serializer.save(user=self.request.user, following=following)
