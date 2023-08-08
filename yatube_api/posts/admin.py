from django.contrib import admin

from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'post',
    )


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author',
        'text', 'pub_date'
    )
    inlines = (
        CommentInline,
    )
