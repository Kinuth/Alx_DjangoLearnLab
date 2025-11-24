from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library
from .models import Book
from django.contrib.auth.decorators import user_passes_test

def list_books(request):
    """
    Retrieves all books from the database and renders a template 
    displaying a list of titles and authors.
    """
    # Fetch all book instances from the database
    books = Book.objects.all()
    
    # Create the context dictionary to pass data to the template
    context = {'books': books}
    
    # Render the template with the context
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- Helper functions to check roles ---
def check_admin(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Admin'

# Helper function to check if a user is a Librarian
def check_librarian(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Librarian'

# Helper function to check if a user is a Member
def check_member(user):
    return user.is_authenticated and getattr(user, 'userprofile', None) and user.userprofile.role == 'Member'

# --- Role-Based Views ---

@user_passes_test(check_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(check_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(check_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')