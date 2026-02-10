from django.shortcuts import render

# Create your views here.

# views.py
from rest_framework import permissions, status, viewsets, serializers
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Movie, Inventory, Rental
from customer.permissions import IsAdmin, IsCustomer
from .serializers import MovieSerializer, RentalSerializer, InventorySerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    @action(detail=True, methods=['post'])
    def return_movie(self, request, pk=None):
        rental = self.get_object()

        if rental.status == 'RETURNED':
            return Response(
                {"error": "Movie already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rental.status = 'RETURNED'
        rental.return_date = now()
        rental.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data, status=status.HTTP_200_OK)

