from django.shortcuts import render, redirect
from .models import Profile,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm,CustomUserChangeForm,ProfileForm
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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
            return redirect('homepage') 
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

# upgrading the roles
"""
Allows a user to upgrade their roles

"""
@login_required
def upgrade_role(request):
    user = request.user
    context = {'user':user}
    
    if request.method == 'POST':
        if 'become_host' in request.POST and not user.is_host:
            user.is_host =True
            user.save()
            context['message'] = "You are now a new Host"
        elif 'become_landlord' in request.POST and not user.is_landlord:
            user.is_landlord = True
            user.save()
            context['message'] = "You are now a new  Landlord"
        elif 'become_seller' in request.POST and not user.is_seller:
            user.is_seller = True
            user.save()
            context['message'] = "You are now a new Buyer"
        else:
            context['error'] = "You can not upgrade a role"
        return render(request, 'accounts/role_upgrade.html', context)
    
    return render(request, 'accounts/role_upgrade.html', context)

# DRF Views
"""
registering
login
End points for viewing and listing
linking a profile to a user
updating the profile to only users to edit their own profile
""" 
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class RegistratioAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.action == 'retrieve' and self.kwargs.get('pk'): #== 'me'
            return self.request.user
        return super().get_object()
class ProfileViewSet(viewsets.ModelViewSet):   
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated] 
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self,serializer):
        if serializer.instance.user == self.request.user:
            serializer.save()
        else:
            self.permission_denied(self.request, message = "You allowed to only edit your profile" )
            
# role upgrades
class RoleUpgradeAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        role_choice_upgrade = request.data.get('role','')
        
        if role_choice_upgrade == 'host' and not user.is_host:
            user.is_host = True
            user.save()
            return Response({'message':'Successfully upgraded to a Host.', 'is_host': True})
        elif role_choice_upgrade == 'landlord' and not user.is_landlord:
            user.is_host = True
            user.save()
            return Response({'message':'Successfully upgraded to a  Landlord.', 'is_landlord': True})
        elif role_choice_upgrade == 'seller' and not user.is_seller:
            user.is_host = True
            user.save()
            return Response({'message':'Successfully upgraded to a  Seller.', 'is_seller': True})
        else:
            return Response({'message': 'Invalid upgrade request.'}, status=status.HTTP_400_BAD_REQUEST)
        