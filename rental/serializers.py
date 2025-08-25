from rest_framework import serializers
from .models import RentalHouse, RentalApplication, LeaseAgreement, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['images',]
        
class RentalHouseSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = RentalHouse
        fields = ['__all__']
        