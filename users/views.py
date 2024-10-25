from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm  # Import the user change form
from django.shortcuts import render

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()     
    return render(request, 'users/register.html', {'form': form})
    

def login_view(request):
    if(request.method == 'POST'): 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('project_list')
        else: 
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')


@login_required
def user_profile(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')  # Redirect back to the profile page
    else:
        form = UserChangeForm(instance=user)

    return render(request, 'users/user_profile.html', {'form': form})

