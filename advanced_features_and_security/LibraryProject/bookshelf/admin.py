from django.contrib import admin
from .models import Book

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

