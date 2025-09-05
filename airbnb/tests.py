from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import Profile
from .models import AirbnbHouse
from django.urls import reverse
# testing the account status 
class AirbnbApiTestCase(APITestCase):
    def setUp(self):
        self.host_user = User.objects.create_user(
            username='hostuser',
            password='hostpass123'
        )
        Profile.objects.create(user=self.host_user, is_host=True)
        
        self.create_user = User.objects.create_user(
            username='customeruser',
            password='customerpass123'
        )
        
        # creating a house by the host
        self.house = AirbnbHouse.objects.create(
            name="Test House",
            host=self.host_user,
            description="A great place to stay.",
            price=1500.00,
            furnishing_style="Fully_Furnished",
            bedroom="2_bedroom",
            bathroom="1_bathroom",
            location="Nairobi",
            rules="No smoking",
            amenities="Wifi, AC"
        )
        self.houses_list_url = reverse('airbnb:airbnb-houses-list')
        self.house_detail_url = reverse('airbnb:airbnb-houses-detail', args=[self.house.pk])
        self.bookings_list_url = reverse('airbnb:house-bookings-list', args=[self.house.pk])
        self.images_list_url = reverse('airbnb:house-images-list', args=[self.house.pk])
        
