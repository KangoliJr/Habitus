from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os
from django.utils import timezone

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
    # house_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
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
        return f"House {self.name} by {self.host.username}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='airbnb_bookings')
    house = models.ForeignKey(AirbnbHouse, on_delete=models.CASCADE, related_name='bookings')
    checkin = models.DateField()
    checkout = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return f"Booking for {self.house.name} by {self.customer.username}"
    
    def clean(self):
        if self.checkin >= self.checkout:
            raise ValidationError("Check-out date must be after check-in date.")

    def __str__(self):
        return f"Booking for {self.house.name} by {self.customer.username}"

    
    def __str__(self):
        status = 'Booked' if self.booking else 'Available'
        return f"{self.house.name}: {self.checkin.strftime('%Y-%m-%d')} to {self.checkout.strftime('%Y-%m-%d')} ({status})"  
# dynamic folder
def house_directory_path(instance, filename):
    sanitized_name = instance.house.name.replace(" ", "_") 
    folder_name = f'{instance.house_id}_{sanitized_name}'
    return os.path.join(f'airbnb/{folder_name}', filename)
    # return os.path.join(f'airbnb/house_{instance.house.pk}', filename)


class Images(models.Model):
    image = models.ImageField(upload_to=house_directory_path)
    house = models.ForeignKey(AirbnbHouse,on_delete=models.CASCADE, related_name='images')
    
    is_primary = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"Image for {self.house.name}"

