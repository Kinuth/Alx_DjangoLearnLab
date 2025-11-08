from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
# Create your views here.
def list_books(request):
    """
    View to list all books. 
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'view_type': 'Function_Based View',
        }

    return render(request, 'relationship_app/list_books.html', context)
class LibraryDetailView(DetailView):
    """
    Detail view for a specific library, showing its books.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Library = self.object()
        context['books'] = Library.books.select_related('author').all()
        context['view_type'] = 'Class_Based DetailView'
        return context
    
    