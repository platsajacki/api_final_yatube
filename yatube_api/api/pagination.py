from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination
)


class PostPaginator(PageNumberPagination, LimitOffsetPagination):
    page_size = 10
