from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm,CustomUserChangeForm,ProfileForm
# Create your views here.
"""
Creating a loging in section after registering
"""
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user)
            auth_login(request, user) 
            return redirect('accounts:user_profile_dashboard') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# authentication processes
@login_required
def user_profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile_view.html', context)

"""
Allowing a registered user to edit  profile details.
"""
@login_required
def user_profile_edit(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:user_profile_view')
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
    
   