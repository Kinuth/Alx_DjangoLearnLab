from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


# --- TASK 1: CUSTOM USER ADMIN ---


class CustomUserAdmin(UserAdmin):
    """Configuration for the CustomUser model in the Django admin."""

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


# --- TASK 2: Book admin registration ---


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year', 'author')


admin.site.register(Book, BookAdmin)


