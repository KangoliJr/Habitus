from django.db import models
from django.conf import settings
import os

class RentalHouse(models.Model):
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
    name = models.CharField(max_length=200)
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_houses')
    description = models.TextField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.FloatField(default=0)
    furnishing_style = models.CharField(max_length=20, choices=FURNISHING_STYLES)
    bedroom = models.CharField(max_length=20, choices=BEDROOM_TYPES)
    bathroom = models.CharField(max_length=20, choices=BATHROOM_TYPES)
    location = models.CharField(max_length=30)
    rules = models.TextField()
    amenities = models.TextField()
    
    def __str__(self):
        return f"House {self.house_id} by {self.landlord.username}"
    

class RentalApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Leased', 'Leased'),
    ]
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rental_application')
    house = models.ForeignKey(RentalHouse, on_delete=models.CASCADE, related_name='application')
    move_in_date = models.DateField()
    lease_duration_months = models.IntegerField(help_text="Duration of the lease in months.")
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.house.house_id} by {self.tenant.username}"
    
class LeaseAgreement(models.Model):
    application = models.OneToOneField(RentalApplication, on_delete=models.CASCADE, related_name='lease_agreement')
    landlord_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='landlord_leases')
    tenant_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_leases')
    start_date = models.DateField()
    end_date = models.DateField()
    is_signed_by_tenant = models.BooleanField(default=False)
    is_signed_by_landlord = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lease for {self.application.house.house_id}"
class Images(models.Model):
    images = models.ImageField(upload_to='house_directory_path')
    house = models.ForeignKey(RentalHouse,on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return f"Image for {self.house.house_id}"
# dynamic folder
def house_directory_path(instance, filename):
    sanitized_name = instance.house.house_id.replace(" ", "_") 
    folder_name = f'house_{sanitized_name}'
    return os.path.join(f'rental/{folder_name}', filename)
