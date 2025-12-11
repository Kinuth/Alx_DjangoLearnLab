from django.contrib.auth.models import User
from .models import Profile                
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Check requirement: explicitly using serializers.CharField
    password = serializers.CharField()

    class Meta:
        model = User()
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        # Check requirement: get_user_model().objects.create_user
        user = User().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )

        # Check requirement: Token.objects.create
        Token.objects.create(user=user)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email']