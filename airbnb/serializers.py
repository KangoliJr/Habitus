from rest_framework import serializers
from .models import AirbnbHouse, Booking, Checkdates, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
        read_only_fields = ['house']
        
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
class CheckdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkdates
        fields = '__all__'
        
class AirbnbHouseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    availability = CheckdatesSerializer(many=True, read_only=True)
    class Meta:
        model = AirbnbHouse
        fields = [
            'host', 'description', 'price', 'furnishing_style',
            'bedroom', 'bathroom', 'location', 'rules', 'amenities',
            'images', 'bookings', 'availability'
        ]