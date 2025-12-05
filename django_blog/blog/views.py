from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.response import Response
from django.http import HttpResponseForbidden


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Homepage view
def home(request):
    context = {
        'posts': Post.objects.all().order_by('-published_date')
    }
    return render(request, 'blog/home.html', context)

# profile management view
@login_required
def profile(request):
    if request.method == 'POST':
        # Pass the POST data and the current user instance to the form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect enables the "Post-Redirect-Get" pattern
            
    else:
        # If GET request, just fill form with current user data
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'blog/profile.html', context)

# Implement crud views for blog posts below (create, read, update, delete)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # 1. Create the object but don't save to DB yet
            post = form.save(commit=False)
            # 2. Assign the logged-in user as the author
            post.author = request.user
            # 3. Save to database
            post.save()
            return redirect('detail_post', pk=post.pk) # Redirect to your list of posts
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def update_post(request, pk):
    # Get the post, ensure the user owns it or return 404
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        # Pass the instance to update existing data
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # No need for commit=False here as author is already set
            form.save()
            return redirect('detail_post', pk=post.pk)
    else:
        # Pre-populate form with existing data
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Update Post'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# Comment views
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Handle the Comment Form Submission
    if request.method == 'POST':
        # You must be logged in to comment
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            # Create comment object but don't save to DB yet
            comment = form.save(commit=False)
            # Assign the current post and current user
            comment.post = post
            comment.author = request.user
            # Save to DB
            comment.save()
            # Redirect back to the same page to show the new comment
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form, # Pass the form to the template
    }
    return render(request, 'blog/post_detail.html', context)
        
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Security: Only the author can edit
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirect back to the post that owns this comment
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    # We reuse the logic, but pass the 'post' object for the "Cancel" button link
    return render(request, 'blog/add_comment.html', {
        'form': form, 
        'post': comment.post 
    })

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk # Save this to redirect later

    # Security: Only the author can delete
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=post_pk)

    return render(request, 'blog/delete_comment.html', {'object': comment})
