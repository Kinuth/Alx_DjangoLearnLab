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
def check_role(user, role):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role

def is_admin(user):
    return check_role(user, 'Admin')

def is_librarian(user):
    return check_role(user, 'Librarian')

def is_member(user):
    return check_role(user, 'Member')

# --- Role-Based Views ---

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')