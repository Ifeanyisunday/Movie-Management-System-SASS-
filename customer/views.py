from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate 
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum, Count

from .models import CustomUser
from .serializers import PublicUserRegisterSerializer, AdminManagedUserSerializer
from .permissions import IsAdmin
from movie_rental.models import Rental

class AnyUserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = PublicUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registered"}, status=201)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role
        })
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdminManagedUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]




class AdminAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_revenue = Rental.objects.filter(
            status='RETURNED'
        ).aggregate(
            total=Sum('movie__price')
        )['total'] or 0

        total_rentals = Rental.objects.count()
        active_rentals = Rental.objects.filter(
            status='RENTED'
        ).count()

        top_movies = (
            Rental.objects
            .values('movie__title')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

