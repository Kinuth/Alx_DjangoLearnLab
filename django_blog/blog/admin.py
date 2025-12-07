from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'short_content')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')

    def short_content(self, obj):
        return obj.content[:50]
