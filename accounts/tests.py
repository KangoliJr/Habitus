from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.
class AccountTests(APITestCase):

    def test_user_registration(self):
        """
        Ensure we can register a new user and profile.
        """
        url = reverse('accounts:api_register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'phone_number': '1234567890',
            'country': 'Kenya'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        
    def test_get_auth_token(self):
        """
        Ensure we can get an authentication token.
        """
        self.test_user_registration()
        url = reverse('accounts:token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_can_change_password(self):
        """
        Ensure an authenticated user can change their password.
        """
        self.test_user_registration() 
        user = User.objects.get(username='testuser')
        url = reverse('accounts:change-password')
        data = {
            'old_password': 'password123',
            'new_password': 'new_password123'
        }
        
        token_url = reverse('accounts:token_obtain_pair')
        token_data = {'username': 'testuser', 'password': 'password123'}
        token_response = self.client.post(token_url, token_data, format='json')
        access_token = token_response.data['access']
        

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('new_password123'))
    
    def test_upgrade_role(self):
        """
        Ensure a user's role can be upgraded.
        """
        self.test_user_registration()
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_host)
        
        url = reverse('accounts:api_upgrade_role')
        data = {'role_to_upgrade': 'host'}
        

        token_url = reverse('accounts:token_obtain_pair')
        token_data = {'username': 'testuser', 'password': 'password123'}
        token_response = self.client.post(token_url, token_data, format='json')
        access_token = token_response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_host)