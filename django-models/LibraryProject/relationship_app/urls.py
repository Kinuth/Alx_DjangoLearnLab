# relationship_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import LibraryDetailView, SignUpView
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'relationship_app'

urlpatterns = [
    # Function-Based View (FBV): Lists all books
    path('books/', views.list_books, name='all_books'),

    # Class-Based View (CBV): Shows details for a specific library
    # The <int:pk> captures the primary key (ID) of the Library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
  
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", SignUpView.as_view(), name="templates/registration/signup"),
    # 1. Registration View (Assuming a custom FBV named 'register')
    path('register/', views.register, name='register'), 

    # 2. Login View (Using Django's built-in CBV and specifying a template name)
    path('login/',
         LoginView.as_view(template_name='relationship_app/login.html'), 
         name='login'),

    # 3. Logout View (Using Django's built-in CBV and specifying a template name for confirmation/redirection)
    path('logout/',
         LogoutView.as_view(template_name='relationship_app/logged_out.html'), 
         
         name='logout'),

    path('admin_area/', views.admin_view, name='admin_view'),
    path('librarian_desk/', views.librarian_view, name='librarian_view'),
    path('member_portal/', views.member_view, name='member_view'),

    # URL pattern for adding a new book
    path('add/book/', views.add_book, name='add_book'),

    # URL pattern for editing an existing book (requires the book's primary key)
    path('edit/book/<int:pk>/', views.edit_book, name='edit_book'),

    # URL pattern for deleting a book (requires the book's primary key)
    path('delete/book/<int:pk>/', views.delete_book, name='delete_book'),
]
