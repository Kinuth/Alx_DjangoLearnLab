from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    """
    Define the admin view for the CustomUser model.
    """
    model = CustomUser
    
    # Use the default UserAdmin fieldsets and add our custom fields
    # We add 'date_of_birth' and 'profile_photo' to the 'Personal info' section
    
    # This is the default fieldsets structure from UserAdmin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add our custom fields to the list display
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    
    # Add our fields to the search fields
    search_fields = ('email', 'first_name', 'last_name')
    
    # Set the ordering (since we removed username)
    ordering = ('email',)

# Register the CustomUser model with our custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
