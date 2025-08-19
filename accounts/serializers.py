from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'age', 'gender', 'phone_number', 'country',
            'is_customer', 'is_host', 'is_landlord', 'is_tenant', 'is_seller', 'is_buyer'
        ]
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']