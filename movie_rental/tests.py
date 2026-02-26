
# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Movie, Inventory, Rental

User = get_user_model()


class AppTests(APITestCase):

    # Create test user
    def setUp(self):

        # create customer
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            role='customer'
        )

         # create vendor
        self.vendor = User.objects.create_user(
            username="vendor",
            password="testpass123",
            role="vendor"
        )

        
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Create a movie
        self.movie = Movie.objects.create(
            title='Inception',
            genre='comedy',
            daily_rate=10,
            release_year=2010,
            price=1000,
            vendor=self.vendor  
        )

        # Create inventory
        self.inventory = Inventory.objects.create(
            movie=self.movie,
            available_copies=5
        )

    def test_rent_movie_success(self):
        url = reverse('rentals-list')
        response = self.client.post(url, {'movie': self.movie.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 1)

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.available_copies, 4)

    def test_rent_movie_out_of_stock(self):
        self.inventory.available_copies = 0
        self.inventory.save()

        url = reverse('rentals-list')
        response = self.client.post(url, {'movie': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_movie(self):
        rental = Rental.objects.create(
            user=self.user,
            movie=self.movie,
            status='RENTED'
        )

        self.inventory.available_copies = 0
        self.inventory.save()

        url = reverse('rentals-return-movie', args=[rental.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rental.refresh_from_db()
        self.assertEqual(rental.status, 'RETURNED')

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.available_copies, 1)


    
    def test_cannot_rent_twice(self):
        self.client.force_authenticate(user=self.user)

        self.client.post("/api/rentals/", {"movie": self.movie.id})
        response = self.client.post("/api/rentals/", {"movie": self.movie.id})

        self.assertEqual(response.status_code, 400)
