from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book
from django.contrib.auth.decorators import permission_required

# --- TASK 2: ENFORCE PERMISSIONS IN VIEWS ---

# This view is protected.
# Only users with the 'bookshelf.can_view' permission can access it.
# This permission can be assigned directly or via a group (e.g., "Viewers").
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Only users with 'bookshelf.can_create' can access this view.
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create_view(request):
    # ... logic for creating a book (e.g., with a ModelForm) ...
    return HttpResponse(f"Create Book Form (User: {request.user})")

# Only users with 'bookshelf.can_edit' can access this view.
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # ... logic for editing a book (e.g., with a ModelForm) ...
    return HttpResponse(f"Editing Book: {book.title} (User: {request.user})")

# Only users with 'bookshelf.can_delete' can access this view.
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # ... logic for deleting a book ...
    return HttpResponse(f"Deleting Book: {book.title} (User: {request.user})")


# --- TASK 3: SECURE DATA ACCESS (AVOIDING SQL INJECTION) ---

def book_search_view(request):
    """
    Demonstrates safe vs. unsafe query building.
    """
    query = request.GET.get('q', '')

    # -------------------------------------------------------------------
    # VULNERABLE TO SQL INJECTION (DO NOT DO THIS)
    # -------------------------------------------------------------------
    # This method uses string formatting to build a raw SQL query.
    # If a user enters: "'; DROP TABLE bookshelf_book; --"
    # the query could become:
    # "SELECT * FROM bookshelf_book WHERE title = ''; DROP TABLE bookshelf_book; --'"
    # This is a classic SQL injection attack.
    
    # unsafe_results = Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title = '{query}'")
    # print("Unsafe query:", unsafe_results.query) # For demonstration

    # -------------------------------------------------------------------
    # SAFE (USING DJANGO ORM)
    # -------------------------------------------------------------------
    # The Django ORM parameterizes the query. This means it separates
    # the query logic from the user-supplied data.
    # The database treats the 'query' variable as data only, not as
    # an executable command. This prevents SQL injection.
    
    safe_results = Book.objects.filter(title__icontains=query)
    
    # This is also safe if you must use raw SQL, as it uses parameters:
    # safe_raw_results = Book.objects.raw("SELECT * FROM bookshelf_book WHERE title = %s", [query])

    return render(request, 'bookshelf/book_search_results.html', {
        'results': safe_results,
        'query': query
    })