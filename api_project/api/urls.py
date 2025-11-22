from django.urls import path
from .views import BookList
from rest_framework import router
from .views import BookViewSet
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

routers = router.DefaultRouter()
routers.register(r'books_all', BookViewSet, basename='book_all')  # Registers the BookViewSet with the router 

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
 # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    ]
