# relationship_app/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Include all fields required for creation and editing
        fields = ['title', 'author']
       