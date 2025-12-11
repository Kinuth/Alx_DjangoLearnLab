from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer # We will create this in Step 6

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer # You need to define this serializer

    def get_queryset(self):
        # Return notifications for the current user, unread first
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
