from django.db import models
from django.conf import settings
import os

class AirbnbHouse(models.Model):
    FURNISHING_STYLES = [
        ('Fully_Furnished', 'Fully Furnished'),
        ('Semi_Furnished', 'Semi Furnished'),
    ]
    
    BEDROOM_TYPES = [
        ('1_bedroom', '1 Bedroom'),
        ('2_bedroom', '2 Bedroom'),
        ('3_bedroom', '3 Bedroom'),
        ('4_bedroom', '4 Bedroom'),
        ('5_bedroom', '5 Bedroom'),
        ('bedsitter', 'Bedsitter'),
        ('other', 'Other'),
    ]
    
    BATHROOM_TYPES = [
        ('1_bathroom', '1 Bathroom'),
        ('2_bathroom', '2 Bathroom'),
        ('3_bathroom', '3 Bathroom'),
        ('4_bathroom', '4 Bathroom'),
        ('all_ensuite', 'All Ensuite'),
        ('other', 'Other'),
    ]
    house_id = models.CharField(max_length=100, primary_key=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='airbnb_houses')
    description = models.TextField()
    price = models.FloatField()
    furnishing_style = models.CharField(max_length=20, choices=FURNISHING_STYLES)
    bedroom = models.CharField(max_length=20, choices=BEDROOM_TYPES)
    bathroom = models.CharField(max_length=20, choices=BATHROOM_TYPES)
    location = models.CharField(max_length=30)
    rules = models.TextField()
    amenities = models.TextField()
    
    def __str__(self):
        return f"House {self.house_id} by {self.host.username}"
    
class Booking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='airbnb_bookings')
    house = models.ForeignKey(AirbnbHouse, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.house.house_id} by {self.customer.username}"
    

class Checkdates(models.Model):
    house = models.ForeignKey(AirbnbHouse, on_delete=models.CASCADE, related_name='availability')
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()  
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_dates')
    
    def __str__(self):
        status = 'Booked' if self.booking else 'Available'
        return f"{self.house.house_id}: {self.checkin.strftime('%Y-%m-%d')} to {self.checkout.strftime('%Y-%m-%d')} ({status})"  
    
class Images(models.Model):
    image = models.ImageField(upload_to='house_directory_path')
    house = models.ForeignKey(AirbnbHouse,on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return f"Image for {self.house.house_id}"
# dynamic folder
def house_directory_path(instance, filename):
    sanitized_name = instance.house.house_id.replace(" ", "_") 
    folder_name = f'house_{sanitized_name}'
    return os.path.join(f'airbnb/{folder_name}', filename)

