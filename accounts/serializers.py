from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'age', 'gender', 'phone_number', 'country',
            'is_customer', 'is_host', 'is_landlord', 'is_tenant', 'is_seller', 'is_buyer'
        ]
        
    def create(self, validated_data):
        extra_fields = {
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
            'date_of_birth': validated_data.get('date_of_birth', None),
            'age': validated_data.get('age', None),
            'gender': validated_data.get('gender', None),
            'phone_number': validated_data.get('phone_number', None),
            'country': validated_data.get('country', None),
            'is_customer': validated_data.get('is_customer', True),
            'is_host': validated_data.get('is_host', False),
            'is_landlord': validated_data.get('is_landlord', False),
            'is_tenant': validated_data.get('is_tenant', True),
            'is_seller': validated_data.get('is_seller', False),
            'is_buyer': validated_data.get('is_buyer', True)
        }
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            **extra_fields
        )
        return user
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']