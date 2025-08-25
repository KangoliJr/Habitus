from rest_framework import serializers
from .models import AirbnbHouse, Booking, Checkdates, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = 'image'
        read_only_fields = ['house']
        
    
class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['customer', 'is_confirmed', 'created_at']
class CheckdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkdates
        fields = '__all__'
        
class AirbnbHouseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    availability = CheckdatesSerializer(many=True, read_only=True)
    
    host = serializers.CharField(source='host.username', read_only=True)
    class Meta:
        model = AirbnbHouse
        fields = [
            'name','host', 'description', 'price', 'furnishing_style',
            'bedroom', 'bathroom', 'location', 'rules', 'amenities',
            'images', 'bookings', 'availability'
        ]
        read_only_fields = ['host']