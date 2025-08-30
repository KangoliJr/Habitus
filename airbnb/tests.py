from django.test import TestCase
from .models import AirbnbHouse, Booking, Images
from ..accounts.models import Profile
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class AirbnbAPITestCase(APITestCase):

    def setUp(self):
        # Create a host user
        self.host_user = User.objects.create_user(
            username='hostuser',
            password='hostpassword123'
        )
        Profile.objects.create(user=self.host_user, is_host=True)

        # Create a regular user (customer)
        self.customer_user = User.objects.create_user(
            username='customeruser',
            password='customerpassword123'
        )
        Profile.objects.create(user=self.customer_user)

        # Create a house listing for the host
        self.house = AirbnbHouse.objects.create(
            name="Test House",
            host=self.host_user,
            description="A great place to stay.",
            price=150.00,
            furnishing_style="Fully_Furnished",
            bedroom="2_bedroom",
            bathroom="1_bathroom",
            location="Nairobi",
            rules="No smoking",
            amenities="Wifi, AC"
        )
        
        # Get URLs
        self.houses_list_url = reverse('airbnb:airbnb-houses-list')
        self.house_detail_url = reverse('airbnb:airbnb-houses-detail', args=[self.house.pk])
        self.bookings_list_url = reverse('airbnb:house-bookings-list', args=[self.house.pk])
        self.images_list_url = reverse('airbnb:house-images-list', args=[self.house.pk])

# -----------------
# AirbnbHouseViewSet Tests
# -----------------

    def test_list_houses(self):
        """
        Ensure public can list all houses.
        """
        response = self.client.get(self.houses_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_house(self):
        """
        Ensure public can retrieve a single house.
        """
        response = self.client.get(self.house_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test House')

    def test_create_house_as_host(self):
        """
        Ensure a host can create a new house.
        """
        self.client.force_authenticate(user=self.host_user)
        data = {
            'name': "New House",
            'description': "A new listing.",
            'price': 200.00,
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
        """
        Ensure a customer cannot create a new house.
        """
        self.client.force_authenticate(user=self.customer_user)
        data = {
            'name': "New House",
            'description': "A new listing."
        }
        response = self.client.post(self.houses_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(AirbnbHouse.objects.count(), 1)

    def test_update_house_as_host(self):
        """
        Ensure a host can update their own house.
        """
        self.client.force_authenticate(user=self.host_user)
        data = {'price': 175.00}
        response = self.client.patch(self.house_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.house.refresh_from_db()
        self.assertEqual(self.house.price, 175.00)

    def test_delete_house_as_host(self):
        """
        Ensure a host can delete their own house.
        """
        self.client.force_authenticate(user=self.host_user)
        response = self.client.delete(self.house_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AirbnbHouse.objects.count(), 0)

# -----------------
# BookingViewSet Tests
# -----------------

    def test_create_booking_as_customer(self):
        """
        Ensure an authenticated user can create a booking.
        """
        self.client.force_authenticate(user=self.customer_user)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        data = {
            'checkin': today.isoformat(),
            'checkout': tomorrow.isoformat()
        }
        response = self.client.post(self.bookings_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().customer, self.customer_user)

    def test_create_booking_conflict(self):
        """
        Ensure a user cannot book a house for dates that are already booked.
        """
        self.client.force_authenticate(user=self.customer_user)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        Booking.objects.create(
            house=self.house,
            customer=self.customer_user,
            checkin=today,
            checkout=tomorrow
        )
        data = {
            'checkin': today.isoformat(),
            'checkout': tomorrow.isoformat()
        }
        response = self.client.post(self.bookings_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This house is already booked for the selected dates.", str(response.data))

# -----------------
# ImagesViewSet Tests
# -----------------

    def test_upload_image_as_host(self):
        """
        Ensure a host can upload an image to their own house.
        """
        self.client.force_authenticate(user=self.host_user)
        image = SimpleUploadedFile(
            "test_image.jpg", 
            b"file_content", 
            content_type="image/jpeg"
        )
        data = {'image': image}
        response = self.client.post(self.images_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Images.objects.count(), 1)
        self.assertEqual(Images.objects.get().house, self.house)
