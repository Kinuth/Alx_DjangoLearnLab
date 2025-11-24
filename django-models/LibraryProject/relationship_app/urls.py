from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Function-based view to list all books
    path('books/', list_books, name='list_books'),

    # Class-based view to show specific library details
    # <int:pk> captures the Primary Key (ID) of the library from the URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Built-in Logout View
    # We specify the template_name so it renders a page after logging out
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Our custom Registration View
    path('register/', views.register, name='register'),
    # Role-based access views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
