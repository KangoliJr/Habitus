from django.test import TestCase, Client
from .models import OwnedHouse, HousePurchase, Images
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
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
        
    def test_onwed_house_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owned_home/owned_house_list.html')
        self.assertContains(response, self.house.name)

    def test_owned_house_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owned_home/owned_house_detail.html')
        self.assertContains(response, self.house.name)
        
    def test_add_owned_house_view_auth(self):
        initial_house_count = OwnedHouse.objects.count()
        self.client.login(username='testowner', password='password123')
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code,200)
        
        post_data = {
            'name': 'New House',
            'description': 'A new will be sold',
            'price': 300000,
            'location': 'Mombasa',
            'furnishing_style': 'Fully_Furnished',
            'bedroom': '3_bedroom',
            'bathroom': '2_bathroom',
            'rules': 'No smoking',
            'amenities': 'Pool'
        }
        response = self.client.post(self.add_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(OwnedHouse.objects.count(),initial_house_count + 1)
        
    def test_edit_owned_house_view_auth(self):
        self.client.login(username='testowner', password='password123')
        post_data={
            'name': 'Updated House',
            'description': 'Updated description',
            'price': 260000,
            'location': 'Nairobi',
            'furnishing_style': 'unfurnished',
            'bedroom': '2_bedroom',
            'bathroom': '1_bathroom',
            'rules': 'No pets',
            'amenities': 'Parking, Balcony'
        }
        response = self.client.post(self.edit_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.house.refresh_from_db()
        self.assertEqual(self.house.name, 'Updated House')

    def test_edit_owned_house_view_permissions(self):
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 404) 

    def test_delete_owned_house_view_auth(self):
        self.client.login(username='testowner', password='password123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(OwnedHouse.objects.count(), 0)

    def test_delete_owned_house_view_permissions(self):
        self.client.login(username='otheruser', password='password123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 404)
        
class OwnedHomeAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='ownerapi', password='password123')
        