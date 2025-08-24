from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password','last_name',
            'date_of_birth', 'age', 'gender', 'phone_number', 'country',
            'is_customer', 'is_host', 'is_landlord', 'is_tenant', 'is_seller', 'is_buyer'
        ]
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']