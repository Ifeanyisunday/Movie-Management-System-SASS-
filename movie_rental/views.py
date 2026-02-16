from django.shortcuts import render

# Create your views here.

# views.py
from rest_framework import permissions, status, viewsets, serializers
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction



from .models import Movie, Inventory, Rental
from customer.permissions import IsAdmin, IsCustomer
from .serializers import MovieSerializer, RentalSerializer, InventorySerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['title']  # search by title


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # return [IsAuthenticated(), IsAdmin()]
            return [IsAdmin()]
        return [IsAuthenticated()]
    

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]



class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        # User only sees their rentals
        return Rental.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        movie = serializer.validated_data['movie']

        # Lock the inventory row
        inventory = Inventory.objects.select_for_update().get(movie=movie)

        if inventory.available_copies <= 0:
            raise serializers.ValidationError({"error": "Movie is out of stock"})

        # Reduce stock safely
        inventory.available_copies -= 1
        inventory.save()

        # Save rental
        serializer.save(user=self.request.user)



    @action(detail=True, methods=['post'])
    @transaction.atomic
    def return_movie(self, request, pk=None):
        rental = self.get_object()

        if rental.status == 'RETURNED':
            return Response(
                {"error": "Movie already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Lock inventory row
        inventory = Inventory.objects.select_for_update().get(
            movie=rental.movie
        )

        rental.status = 'RETURNED'
        rental.return_date = now()
        rental.save()

        # Increase stock
        inventory.available_copies += 1
        inventory.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data, status=status.HTTP_200_OK)

