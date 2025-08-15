from django.db import models
import os

# Create your models here.
class Owner(models.Model):
    owner_id = models.CharField(max_length=20, primary_key=True)
    owner_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.owner_name
    
class Buyer(models.Model):
    buyer_id = models.CharField(max_length=100, primary_key=True)
    buyer_name = models.CharField(max_length=100)
    def __str__(self):
        return self.buyer_name

class OwnedHouse(models.Model):
    FURNISHING_STYLES = [
        ('Fully_Furnished', 'Fully Furnished'),
        ('Semi_Furnished', 'Semi Furnished'),
        ('None_Furnished', 'None Furnished'),
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
    owner_name = models.ForeignKey(Owner,on_delete=models.CASCADE, related_name='houses')
    description = models.TextField()
    price = models.FloatField()
    furnishing_style = models.CharField(max_length=20, choices=FURNISHING_STYLES)
    bedroom = models.CharField(max_length=20, choices=BEDROOM_TYPES)
    bathroom = models.CharField(max_length=20, choices=BATHROOM_TYPES)
    location = models.CharField(max_length=30)
    rules = models.TextField()
    amenities = models.TextField()
    
    def __str__(self):
        return f"House {self.house_id} by {self.owner_name}"
    
class Images(models.Model):
    images = models.ImageField(upload_to='house_directory_path')
    house = models.ForeignKey(OwnedHouse,on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return f"Image for {self.house.house_id}"
# dynamic folder
def house_directory_path(instance, filename):
    sanitized_name = instance.house.house_id.replace(" ", "_") 
    folder_name = f'house_{sanitized_name}'
    return os.path.join(f'owned_home/{folder_name}', filename)