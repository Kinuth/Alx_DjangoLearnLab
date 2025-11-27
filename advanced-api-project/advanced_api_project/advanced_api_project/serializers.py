from django.db import models
from rest_framework import serializers
from .models import Author, Book

# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

# Serializer for Book model with nested Author details
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()  # Nested serializer to include author details

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date']

    def validate (self, data):
        # Example validation: Ensure published_date is not in the future
        from datetime import date
        if data['published_date'] > date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return data