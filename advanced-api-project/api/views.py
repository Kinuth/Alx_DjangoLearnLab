from django.shortcuts import render
from django_filters import rest_framework
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    """
    View to retrieve a list of all books.
    
    Permissions:
    - AllowAny: Accessible to both authenticated and unauthenticated users.
    
    Features:
    - Advanced filtering (by title, author, publication_year).
    - Search functionality.
    - Ordering capability.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission: Unauthenticated users can view the list
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Features: Filtering, Searching, and Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Fields allowed for filtering
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Fields allowed for searching (keywords)
    search_fields = ['title', 'author']
    
    # Fields allowed for ordering
    ordering_fields = ['title', 'publication_year']

   
# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    
    Permissions:
    - AllowAny: Accessible to both authenticated and unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    # Permission: Unauthenticated users can view details
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    
    Permissions:
    - IsAuthenticated: Only logged-in users can create books.
    
    Custom Behavior:
    - Validates that the publication year is not in the future (custom logic example).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission: Locked down to authenticated users
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Customizes the creation process.
        This hook allows us to add custom logic before saving the instance.
        """
        # Example custom validation or data modification
        # functionality: "Customize... to ensure they properly handle form submissions"
        title = serializer.validated_data.get('title')
        print(f"Creating a new book titled: {title}") # Debug/Log output
        
        # Save the data (the serializer handles basic validation automatically)
        serializer.save()

# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    
    Permissions:
    - IsAuthenticated: Only logged-in users can modify books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    # Permission: Locked down to authenticated users
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Customizes the update process.
        """
        # Example: Log the update
        instance = serializer.instance
        print(f"Updating book: {instance.title}")
        
        serializer.save()

# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    
    Permissions:
    - IsAuthenticated: Only logged-in users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    # Permission: Locked down to authenticated users
    permission_classes = [IsAuthenticated]
   
