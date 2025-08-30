from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_host = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_tenant = models.BooleanField(default=True)
    is_buyer = models.BooleanField(default=True)
    def __str__(self):
        return self.username
    
    
    
class Profile(models.Model):
    GENDER_TYPE =[
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER_TYPE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self):
        return f"Your new Profile {self.user.username}"