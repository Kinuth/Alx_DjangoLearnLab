from rest_framework import serializers
from .models import Author, Book

# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True) # Nested representation of Author

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'Published_year']

    # Validation for Published_year to ensure it's not in the future
    def validate_Published_year(self, value):
        from datetime import date
        if value.year > date.today().year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value