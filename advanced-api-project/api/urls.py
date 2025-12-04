from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books (GET)
    path('', BookListView.as_view(), name='book-list'),

    # Retrieve a single book (GET)
    path('', BookDetailView.as_view(), name='book-detail'),

    # Create a new book (POST)
    path('', BookCreateView.as_view(), name='book-create'),

    # Update a book (PUT/PATCH)
    path('', BookUpdateView.as_view(), name='book-update'),

    # Delete a book (DELETE)
    path('', BookDeleteView.as_view(), name='book-delete'),
]