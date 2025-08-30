from django.shortcuts import render, redirect
from .models import Profile,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm,CustomUserChangeForm,ProfileForm
from .serializers import UserRegistrationSerializer, UserProfileSerializer,PasswordChangeSerializer, RoleUpgradeSerializer
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
"""
Creating a loging in section after registering
"""
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect('homepage')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()
    
    # Define the context here, outside the if/else blocks
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/register.html', context)
    
# authentication processes
@login_required
def user_profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    # return redirect('homepage')
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

# DRF Views
"""
registering
login
End points for viewing and listing
linking a profile to a user
updating the profile to only users to edit their own profile
""" 
class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        
    
class ProfileViewSet(viewsets.ModelViewSet):   
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] 
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self,serializer):
        serializer.save()
            
# role upgrades
class RoleUpgradeAPIView(generics.GenericAPIView):
    serializer_class = RoleUpgradeSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        role = serializer.validated_data['role_to_upgrade']
        
        role_map = {
            'host': 'is_host',
            'landlord': 'is_landlord',
            'seller': 'is_seller',
        }
        
        role_attr = role_map[role]
        
        if getattr(user, role_attr):
            return Response({'message': f'You are already a {role}.'}, status=status.HTTP_400_BAD_REQUEST)

        setattr(user, role_attr, True)
        user.save()
        
        return Response({'message': f'Your role has been upgraded to {role} successfully.'}, status=status.HTTP_200_OK)
