from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer
from posts.serializers import PostSerializer    

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp', 'is_read']

    def get_target(self, obj):
        # A simple way to represent the target object (Post, User, etc.)
        return str(obj.target)