from django.contrib import admin
from .models import Post, Comment, Like, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('author', 'content_preview', 'has_image', 'has_video', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('author__username', 'content')

    def content_preview(self, obj):
        return obj.content[:60] if obj.content else '—'
    content_preview.short_description = 'Content'

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Image?'

    def has_video(self, obj):
        return bool(obj.video)
    has_video.boolean = True
    has_video.short_description = 'Video?'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
