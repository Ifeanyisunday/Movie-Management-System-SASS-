from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from customer.models import CustomUser

class AuthTests(APITestCase):

    def test_customer_register(self):

        url = "/api/auth/register/"

        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "phone": "08012345678",
            "role": "customer"
        }

        response = self.client.post(url, data, format="json")

        print(response.data)

        self.assertEqual(response.status_code, 201)