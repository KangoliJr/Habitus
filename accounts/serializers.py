from rest_framework import serializers
from .models import User, Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password',
            'date_of_birth', 'age', 'gender', 'phone_number', 'country',
        ]
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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
    role = serializers.ChoiceField(
        choices=['host', 'landlord', 'seller'],
        required=True
    )
            
        
        