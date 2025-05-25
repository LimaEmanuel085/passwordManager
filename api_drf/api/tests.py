from django.test import TestCase
from django.urls import reverse

class HashPasswordAPITest(TestCase):
    def test_hash_password_success(self):
        url = reverse('hash')
        response = self.client.post(url, {'password': 'admin123'}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('hashed_password', response.json())

    def test_hash_password_not_provided(self):
        url = reverse('hash')
        response = self.client.post(url, {'password': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Password is required')

class VerifyPasswordAPITest(TestCase):
    def test_verify_password_success(self):
        url = reverse('hash')
        response = self.client.post(url, {'password': 'admin123'}, content_type='application/json')
        data = response.json()
        url = reverse('verify')
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['valid'], True)

    def test_verify_password_not_provided(self):
        url = reverse('hash')
        response = self.client.post(url, {'password': 'admin123'}, content_type='application/json')
        url = reverse('verify')
        response = self.client.post(url, {
            'password': '',
            'hashed_password': response.json()['hashed_password']
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Password and hashed password are required')

    def test_verify_hashed_not_provided(self):
        url = reverse('hash')
        response = self.client.post(url, {'password': 'admin123'}, content_type='application/json')
        url = reverse('verify')
        response = self.client.post(url, {
            'password': 'admin123',
            'hashed_password': ''
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Password and hashed password are required')