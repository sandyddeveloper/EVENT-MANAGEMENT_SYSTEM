from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a user for authentication tests
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client = APIClient()

    def test_register_user(self):
        """
        Test user registration endpoint.
        """
        url = reverse('register')  # Updated to match the 'register' URL name in urls.py
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Check that a new user was created

    def test_user_login(self):
        """
        Test user login with valid credentials.
        """
        url = reverse('token_obtain_pair')  # Updated to match the 'token_obtain_pair' URL name in urls.py
        data = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Assuming you're using JWT tokens for authentication
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        url = reverse('token_obtain_pair')  # Updated to match the 'token_obtain_pair' URL name in urls.py
        data = {
            "username": self.user_data['username'],
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_protected_endpoint_with_token(self):
        """
        Test accessing a protected endpoint with a valid token.
        """
        # First login to get a JWT token
        login_url = reverse('token_obtain_pair')  # Updated to match the 'token_obtain_pair' URL name in urls.py
        login_data = {
            "username": self.user_data['username'],
            "password": self.user_data['password']
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['access']

        # Now test a protected endpoint
        protected_url = reverse('events:event-list')  # Update with the actual protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(protected_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint_without_token(self):
        """
        Test accessing a protected endpoint without a token.
        """
        protected_url = reverse('events:event-list')  # Update with the actual protected endpoint
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """
        Test logout endpoint (if implemented).
        """
        # Logout isn't strictly required for JWT-based auth, but if you have a logout endpoint:
        logout_url = reverse('auth:logout')  # Adjust if you have a logout URL
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_invalid(self):
        """
        Test user registration with invalid data.
        """
        url = reverse('register')  # Updated to match the 'register' URL name in urls.py
        data = {
            "username": "newuser",
            "email": "notanemail",
            "password": "short"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
