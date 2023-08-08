from django.contrib import admin

from .models import Post, Group, Comment


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'text', 'post',
    )


@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'slug', 'description',
    )
    inlines = (
        PostInline,
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'text',
        'pub_date', 'group',
    )
    inlines = (
        CommentInline,
    )
