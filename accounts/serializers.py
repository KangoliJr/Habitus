from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class Profile(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'