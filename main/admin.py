from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db.models import Count

from .models import Profile, Book, Tweet


# # Unregister Groups
# admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile


# # Extend User Model
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff']
#     list_display = ['username', 'email', 'first_name', 'last_name']
#     inlines = [ProfileInline]
#
#
# # Unregister initial User
# admin.site.unregister(User)

# Register again User and Profile
# admin.site.register(User, UserAdmin)
admin.site.register(Profile)


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    model = Tweet
    fields = ['user', 'body', 'likes']
    list_display = ['user', 'short_body', 'created_at', 'get_likes', 'updated_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
