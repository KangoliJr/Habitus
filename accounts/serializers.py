from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'date_of_birth', 'age', 'gender', 'phone_number', 'country']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        profile_data = {
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
            'date_of_birth': validated_data.pop('date_of_birth', None),
            'age': validated_data.pop('age', None),
            'gender': validated_data.pop('gender', ''),
            'phone_number': validated_data.pop('phone_number', ''),
            'country': validated_data.pop('country', ''),
        }
        
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        
class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 
                  'date_of_birth', 'age', 'gender', 'country', 'profile'
                ]
        read_only_fields = ['username', 'id']
        
    def update(self,instance, validated_data):
        profile_data = validated_data('profile',None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if profile_data:
            profile_instance = instance.profile
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()
            
        return instance
    
class RoleUpgradeSerializer(serializers.Serializer):
    ROLE_CHOICES = [
        ('host', 'Host'),
        ('landlord', 'Landlord'),
        ('seller', 'Seller'),
    ]
    role_to_upgrade = serializers.ChoiceField(choices=ROLE_CHOICES)
            
        
        