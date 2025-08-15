from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    GENDER_TYPE =[
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_TYPE)
    phone_number = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Welcome to Habitus{self.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    
    def __str__(self):
        return f"Your new Profile!! {self.user.username}"