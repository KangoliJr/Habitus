from rest_framework import serializers
from .models import AirbnbHouse, Booking,Images
from django.core.exceptions import ValidationError


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
        fields = [
            'id', 'house', 'checkin', 'checkout', 'status', 'created_at',
            'customer_username', 'house_name'
        ]
        read_only_fields = ['id', 'customer', 'house', 'status''created_at']
        
    def validate(self, data):
        checkin_date = data.get('checkin')
        checkout_date = data.get('checkout')
        house = data.get('house')
        
        # Check for booking conflicts
        if Booking.objects.filter(
            house=house,
            checkout__gt=checkin_date,
            checkin__lt=checkout_date
        ).exists():
            raise serializers.ValidationError("This house is already booked for the selected dates.")
        
        return data

class AirbnbHouseSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    bookings = BookingSerializer(many=True, read_only=True)
    host = serializers.CharField(source='host.username', read_only=True)
    class Meta:
        model = AirbnbHouse
        fields = [
            'id','name','host', 'description', 'price', 'furnishing_style',
            'bedroom', 'bathroom', 'location', 'rules', 'amenities',
            'images', 'bookings'
        ]
 