from django.shortcuts import render
from .models import Post, Comment
from rest_framework import viewsets, permissions, filters, generics
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly 
from .pagination import StandardResultsSetPagination

# ViewSet for Post model
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']

    def get_serializer_class(self):
        from .serializers import PostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
# ViewSet for Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        from .serializers import CommentSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# View for User Feed
class UserFeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get the list of users the current user is following
        following_users = self.request.user.following.all()
        
        # Filter posts where the author is in the 'following_users' list
        # Order by creation date (descending)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')