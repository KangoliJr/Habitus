from rest_framework import serializers
from .models import AirbnbHouse, Booking,Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image', 'is_primary', 'position']
        read_only_fields = ['house']
        
    
class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    house = serializers.CharField(source='house.name', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['id', 'customer', 'house', 'status''created_at']

class AirbnbHouseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    host = serializers.CharField(source='host.username', read_only=True)
    class Meta:
        model = AirbnbHouse
        fields = [
            'name','host', 'description', 'price', 'furnishing_style',
            'bedroom', 'bathroom', 'location', 'rules', 'amenities',
            'images', 'bookings', 'availability'
        ]
        read_only_fields = ['host']