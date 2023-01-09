from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Book

# Unregister Groups
admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_superuser']
    list_display = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Register again User and Profile
admin.site.register(User, UserAdmin)
admin.site.register(Profile)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
