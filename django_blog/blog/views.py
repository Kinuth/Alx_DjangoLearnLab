from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib import messages

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
    return render(request, 'users/register.html', {'form': form})

# Homepage view
def home(request):
    return render(request, 'users/home.html')

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

    return render(request, 'users/profile.html', context)
        
    
