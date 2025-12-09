from django.urls import path
from .views import UserRegistrationView, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView ,
)   
from .views import CustomTokenObtainPairView

urlpatterns = [
    #   Registration and JWT token endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/',  CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]