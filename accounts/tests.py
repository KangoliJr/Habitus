from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail

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
            'email': 'test@gmail.com',
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

    def test_user_can_request_password_reset(self):
        self.test_user_registration()
        url = reverse('accounts:api_password_reset')
        response = self.client.post(url, {'email': 'test@gmail.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

    def test_user_can_confirm_password_reset(self):
        self.test_user_registration()
        user = User.objects.get(username='testuser')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('accounts:api_password_reset_confirm')
        response = self.client.post(
            url,
            {'uid': uid, 'token': token, 'new_password': 'brandNewPass123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password('brandNewPass123'))


class AccountWebPasswordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='webuser',
            email='webuser@example.com',
            password='password123',
        )

    def test_forgot_password_page_loads(self):
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_sends_email(self):
        response = self.client.post(
            reverse('accounts:password_reset'),
            {'email': 'webuser@example.com'},
        )
        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

    def test_logged_in_user_can_change_password(self):
        self.client.login(username='webuser', password='password123')
        response = self.client.post(
            reverse('accounts:password_change'),
            {
                'old_password': 'password123',
                'new_password1': 'brandNewPass123',
                'new_password2': 'brandNewPass123',
            },
        )
        self.assertRedirects(response, reverse('accounts:password_change_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('brandNewPass123'))