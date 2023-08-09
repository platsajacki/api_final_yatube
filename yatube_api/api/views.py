from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from .serializers import PostSerializer
from posts.models import Post


class UpdateDestroyMixin:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
