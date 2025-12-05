from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
    return render(request, 'blog/home.html')

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
    

        
    
