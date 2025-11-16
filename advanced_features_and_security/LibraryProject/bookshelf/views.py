from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book
from django.contrib.auth.decorators import login_required, permission_required
from .forms import SearchForm

# View to list all articles
@login_required
@permission_required('content.can_view', raise_exception=True)
def book_list(request):
    articles = Article.objects.all()
    return render(request, 'content/article_list.html', {'articles': articles})

# View for a single article detail
@login_required
@permission_required('content.can_view', raise_exception=True)
def book_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'content/article_detail.html', {'article': article})

# View to create a new article
@login_required
@permission_required('content.can_create', raise_exception=True)
def book_create(request):
    # if request.method == 'POST':
    #     form = ArticleForm(request.POST)
    #     if form.is_valid():
    #         article = form.save(commit=False)
    #         article.author = request.user
    #         article.save()
    #         return redirect('article_detail', pk=article.pk)
    # else:
    #     form = ArticleForm()
    # return render(request, 'content/article_form.html', {'form': form})
    
    # Simplified view for demonstration
    return render(request, 'content/article_form.html', {'form': 'Your ArticleForm would be here'})

# View to edit an existing article
@login_required
@permission_required('content.can_edit', raise_exception=True)
def book_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # if request.method == 'POST':
    #     form = ArticleForm(request.POST, instance=article)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('article_detail', pk=article.pk)
    # else:
    #     form = ArticleForm(instance=article)
    # return render(request, 'content/article_form.html', {'form': form})
    
    # Simplified view for demonstration
    return render(request, 'content/article_form.html', {'form': 'Your ArticleForm would be here', 'article': article})

# View to delete an article
@login_required
@permission_required('content.can_delete', raise_exception=True)
def book_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # if request.method == 'POST':
    #     article.delete()
    #     return redirect('article_list')
    # return render(request, 'content/article_confirm_delete.html', {'article': article})
    
    # Simplified view for demonstration
    return render(request, 'content/article_confirm_delete.html', {'article': article})


def book_search(request):
    """
    A view to search for books.
    This view demonstrates secure data handling.
    """
    query = None
    results = []

    if 'query' in request.GET:
        # Step 3: Use a form to validate and sanitize user input.
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            
            # -------------------------------------------------------------
            # Step 3: Secure Data Access (Preventing SQL Injection)
            # -------------------------------------------------------------
            
            # THE RIGHT WAY (Secure): Use the Django ORM.
            # The ORM parameterizes queries, which means the user's
            # input is treated as data, NOT as executable SQL code.
            # This effectively stops all SQL injection attacks.
            
            results = Book.objects.filter(title__icontains=query)

            # -------------------------------------------------------------
            # THE WRONG WAY (INSECURE): Never do this!
            # -------------------------------------------------------------
            #
            # from django.db import connection
            #
            # # This is VULNERABLE to SQL injection.
            # # A user could enter: "'; DROP TABLE bookshelf_book; --"
            #
            # with connection.cursor() as cursor:
            #     cursor.execute(f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'")
            #     results = cursor.fetchall()
            # -------------------------------------------------------------
            
        else:
            # Form is invalid, 'results' will remain empty.
            # You could also pass form.errors to the template.
            pass

    # 'query' is the sanitized data from the form,
    # so it's safer to render back to the template if needed.
    return render(request, 'bookshelf/book_list.html', {
        'books': results,
        'query': query
    })
