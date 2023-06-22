from django.contrib import admin

from .models import Post


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    fields = ['title', 'subtitle', 'slug', 'author', 'content', 'status', 'count', 'tags']
    list_display = ['author', 'short_title', 'status', 'count', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['author', 'title', 'slug', 'tags']
