# relationship_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import LibraryDetailView, SignUpView
from .views import list_books


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
]
