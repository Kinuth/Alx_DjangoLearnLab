from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from notifications.models import Notification
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
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
    
class LikePostView(generics.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post =generics.get_object_or_404(Post, pk=pk)
        
        # Create Like
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Notification (Only if the user isn't liking their own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_200_OK)

class UnlikePostView(generics.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()
            return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)