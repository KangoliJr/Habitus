from django.test import TestCase, Client
from .models import OwnedHouse, HousePurchase, Images
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
# Create your tests here.

class OwnedHomeModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='testowner', password='password123')
        self.buyer = User.objects.create_user(username='testbuyer', password='password123')
        self.house = OwnedHouse.objects.create(
            owner=self.owner,
            name='Test House',
            description='A lovely test house.',
            price=250000,
            location='Nairobi',
            furnishing_style='unfurnished',
            bedroom='2_bedroom',
            bathroom='1_bathroom',
            rules='No rules',
            amenities='Parking, Balcony'
        )
        self.image = Images.objects.create(house=self.house, image='test_image.jpg')
        self.purchase = HousePurchase.objects.create(house=self.house, buyer=self.buyer)

    def test_owned_house_str(self):
        self.assertEqual(str(self.house), "House Test House by testowner")

    def test_images_str(self):
        self.assertEqual(str(self.image), "Image for Test House")

    def test_house_purchase_str(self):
        self.assertEqual(str(self.purchase), "Purchase of Test House by testbuyer")
        
class OwnedHomeTraditionalViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='testowner', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.house = OwnedHouse.objects.create(
            owner=self.owner,
            name='Test House',
            description='A lovely test house.',
            price=250000,
            location='Nairobi',
            furnishing_style='unfurnished',
            bedroom='2_bedroom',
            bathroom='1_bathroom',
            rules='No pets',
            amenities='Parking, Balcony'
        )
        self.list_url = reverse('owned_home:owned_house_list')
        self.detail_url = reverse('owned_home:owned_house_detail', args=[self.house.id])
        self.add_url = reverse('owned_home:add_owned_house')
        self.edit_url = reverse('owned_home:edit_owned_house', args=[self.house.id])
        self.delete_url = reverse('owned_home:delete_owned_house', args=[self.house.id])
