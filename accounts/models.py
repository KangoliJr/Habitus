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
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_TYPE)
    phone_number = models.IntegerField()
    country = models.CharField(max_length=100)
    
    # Role-Based actions
    is_customer = models.BooleanField(default=True)
    is_host = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        # help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        # help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    
    def __str__(self):
        return f"Your new Profile {self.user.username}"