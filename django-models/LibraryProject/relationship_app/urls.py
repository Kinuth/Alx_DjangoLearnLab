# relationship_app/urls.py
from django.urls import path
from . import views
from .views import LibraryDetailView
from .views import book_list


app_name = 'relationship_app'

urlpatterns = [
    # Function-Based View (FBV): Lists all books
    path('books/', views.all_books_list, name='all_books'),

    # Class-Based View (CBV): Shows details for a specific library
    # The <int:pk> captures the primary key (ID) of the Library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]