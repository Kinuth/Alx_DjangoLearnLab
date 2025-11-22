from rest_framework import serializers
from .models import book as Book


class BookSerializer(serializers.ModelSerializer):
        class Meta:
                model = Book
                fields = '__all__'

