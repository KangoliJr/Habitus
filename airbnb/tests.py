from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.models import Profile
from .models import AirbnbHouse
from django.urls import reverse
from rest_framework import status
# testing the account status 
class AirbnbApiTestCase(APITestCase):
    def setUp(self):
        self.host_user = User.objects.create_user(
            username='hostuser',
            password='hostpass123'
        )
        Profile.objects.create(user=self.host_user, is_host=True)
        
        self.customer_user = User.objects.create_user(
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
        
    # airbnb viewsets
    """
    Will test if any one can see all the houses
    Anyone can get a single house unit
    make sure a host can add a house
    see if a customer can create a house; which it should fail
    a host can delete a house unit
    a host can update a house unit
    """
    def test_list_houses(self):
            response = self.client.get(self.houses_list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
    def test_retrieve_house(self):
            response = self.client.get(self.house_detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Test House')

    def test_create_house_as_host(self):
        self.client.force_authenticate(user=self.host_user)
        data = {
            'name': "New House",
            'description': "A new house unit.",
            'price': 2000.00,
            'furnishing_style': "Semi_Furnished",
            'bedroom': "3_bedroom",
            'bathroom': "2_bathroom",
            'location': "Mombasa",
            'rules': "No pets",
            'amenities': "Parking"
        }
        response = self.client.post(self.houses_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AirbnbHouse.objects.count(), 2)

    def test_create_house_as_customer(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'name': "New House",
            'description': "A new listing."
        }
        response = self.client.post(self.houses_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(AirbnbHouse.objects.count(), 1)

    def test_update_house_as_host(self):
        self.client.force_authenticate(user=self.host_user)
        data = {'price': 175.00}
        response = self.client.patch(self.house_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.house.refresh_from_db()
        self.assertEqual(self.house.price, 175.00)

    def test_delete_house_as_host(self):
        self.client.force_authenticate(user=self.host_user)
        response = self.client.delete(self.house_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AirbnbHouse.objects.count(), 0)