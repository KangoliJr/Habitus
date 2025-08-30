from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

# Form for user registration
"""
creating a form for user registration when creating a new user
Editing your user details
adding profile details; picture
"""
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

# editing your user details
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


# Customizing your profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 
            'phone_number', 'country', 'bio', 'profile_picture'
        ]