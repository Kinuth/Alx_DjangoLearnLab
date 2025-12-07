from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(template_name='blog/post_detail.html'), name='detail_post'),
    path('post/<int:pk>/update/', views.update_post, name= 'update_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(template_name='blog/post_delete.html'), name='delete_post'),      
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('search/', views.search_posts, name='search_posts'),
    path('tags/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
]
