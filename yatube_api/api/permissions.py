from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
        )
