from rest_framework import serializers
from .models import OwnedHouse, HousePurchase, Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image',]
        read_only_fields = ['house']

class OwnedHouseSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = OwnedHouse
        fields = ['id', 'owner', 'owner_name', 'name', 'description', 
            'price', 'furnishing_style', 'bedroom', 
            'bathroom', 'location', 'rules', 'amenities', 
            'images']
        read_only_fields = ['owner']
    
class HousePurchaseSerializer(serializers.ModelSerializer):
    house_name = serializers.CharField(source='house.name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    owner_name = serializers.CharField(source='house.owner.username', read_only=True)
    class Meta:
        model = HousePurchase
        fields = [
            'id', 'house', 'house_name', 'buyer', 
            'status', 'purchase_date', 'owner_name', 'buyer_name'
        ]
    read_only_fields = ['status', 'buyer_name', 'purchase_date', 'owner_name']
    

