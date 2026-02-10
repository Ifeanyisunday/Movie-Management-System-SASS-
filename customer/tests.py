from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from customer.models import CustomUser

class AuthTests(APITestCase):
    def test_customer_register(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'john',
            'password': 'pass1234',
            'email': 'john@example.com',      
            'role': 'customer'                
        })

        self.assertEqual(response.status_code, 201)
