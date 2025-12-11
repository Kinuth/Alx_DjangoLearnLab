from django.urls import path
from .views import RegisterView, CustomAuthToken, ProfileView, FollowUserView, UnfollowUserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
]