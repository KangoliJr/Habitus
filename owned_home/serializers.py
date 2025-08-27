from rest_framework import serializers
from .models import OwnedHouse, HousePurchase, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image',]

class OwnedHouseSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    
    class Meta:
        model = OwnedHouse
        fields = ['id', 'owner', 'name', 'description', 
            'price', 'furnishing_style', 'bedroom', 
            'bathroom', 'location', 'rules', 'amenities', 
            'images']
    
class HousePurchaseSerializier(serializers.ModelSerializer):
    house_name = serializers.CharField(source='house.name', read_only=True)
    
    class Meta:
        model = HousePurchase
        fields = [
            'id', 'house', 'house_name', 'buyer', 
            'status', 'purchase_date'
        ]
    

