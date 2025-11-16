from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book
from django.contrib.auth.decorators import login_required, permission_required


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