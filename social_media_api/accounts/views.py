from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import  ProfileSerializer, UserSerializer
from rest_framework.response import Response

# Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return the token in the response immediately after registration
        token = Token.objects.get(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

# Custom Login View (Optional, or use DRF's built-in)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer 
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
  
