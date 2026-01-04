from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse

CustomUser = get_user_model()

class UserViewsTestCase(APITestCase):
    def setUp(self):
        # Creating a test user
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

        # Initialize the APIClient
        self.client = APIClient()

    def test_user_registration(self):
        # Test the user registration endpoint
        registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
        }
        
        register_url = reverse('registrationView')
        response = self.client.post(register_url, 
                                    registration_data, 
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertNotIn('password', response.data)  # password should not be returned

    def test_user_login_successful(self):
        # Test the user login endpoint
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_url = reverse('loginView')
        response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('access', response.data)  # Token should be returned
        self.assertIn('refresh', response.data)  # Token should be returned

    def test_user_login_invalid_credentials(self):
        # Test login with invalid credentials
        invalid_login_data = {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }

        login_url = reverse('loginView')
        response = self.client.post(login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout_successful(self):
        # Test the user logout endpoint
        refresh = RefreshToken.for_user(self.user)
        header = {'HTTP_AUTHORIZATION' : f'Bearer {refresh.access_token}'}

        # Log out the user by invalidating the refresh token
        logout_url = reverse('logoutView')
        response = self.client.post(logout_url, {'refresh': str(refresh)}, 
                                                format='json', 
                                                **header)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_logout_no_token(self):
        # Test logout with no token provided
        logout_url = reverse('logoutView')
        response = self.client.post(logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
