from django.contrib import admin
from .models import Book
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

# Define a custom admin class for the Book model
class BookAdmin(admin.ModelAdmin):
    """
    Customizes the display, search, and filtering options
    for the Book model in the Django admin interface.
    """
    
    # 1. Customize the list view
    # This controls which fields are displayed on the admin's list page
    list_display = ('title', 'author', 'publication_year')
    
    # 2. Add search capabilities
    # This adds a search bar that will search across the 'title' and 'author' fields
    search_fields = ('title', 'author')
    
    # 3. Add filters
    # This adds a filter sidebar, allowing users to filter by publication year or author
    list_filter = ('publication_year', 'author')

# Register the Book model with the custom BookAdmin class
# This tells Django to use the 'BookAdmin' options when displaying the 'Book' model
admin.site.register(Book, BookAdmin)

