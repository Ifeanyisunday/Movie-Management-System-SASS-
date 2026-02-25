from django.shortcuts import render

# Create your views here.

# views.py
from rest_framework import permissions, status, viewsets, serializers
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


from .models import Movie, Inventory, Rental
from .filters import MovieFilter
from customer.permissions import IsAdmin, IsCustomer, IsOwnerVendor, IsVendor
from .serializers import MovieSerializer, RentalSerializer, InventorySerializer


    

# @method_decorator(cache_page(60 * 5), name="list")
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'price']
    filterset_class = MovieFilter
    

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Movie.objects.none()

        if user.role == "vendor":
            return Movie.objects.filter(vendor=user)

        return Movie.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsVendor]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsVendor, IsOwnerVendor]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        movie = serializer.save(vendor=self.request.user)
        Inventory.objects.create(movie=movie, available_copies=0, total_copies=0)

    


    

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']

    def get_queryset(self):
        user = self.request.user
    
        if not user.is_authenticated:
            return Inventory.objects.none()

        if user.role == "vendor":
            return Inventory.objects.filter(movie__vendor=user)

        return Inventory.objects.all()
    

    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsVendor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]



class RentalViewSet(viewsets.ModelViewSet):
    serializer_class = RentalSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Rental.objects.none()

        if user.role == "customer":
            return Rental.objects.filter(user=user)

        if user.role == "vendor":
            return Rental.objects.filter(movie__vendor=user)

        return Rental.objects.all()  # admin

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsCustomer]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @transaction.atomic
    def perform_create(self, serializer):
        movie = serializer.validated_data['movie']

        inventory = Inventory.objects.select_for_update().get(movie=movie)

        if inventory.available_copies <= 0:
            raise serializers.ValidationError(
                {"error": "Movie is out of stock"}
            )

        inventory.available_copies -= 1
        inventory.save()

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

        inventory = Inventory.objects.select_for_update().get(
            movie=rental.movie
        )

        rental.status = 'RETURNED'
        rental.return_date = now()
        rental.save()

        inventory.available_copies += 1
        inventory.save()

        serializer = self.get_serializer(rental)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='vendor')
    def vendor_rentals(self, request):
        rentals = Rental.objects.filter(movie__vendor=request.user)
        page = self.paginate_queryset(rentals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(rentals, many=True)
        return Response(serializer.data)


class HealthCheckViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def status(self, request):
        return Response({"status": "ok"})