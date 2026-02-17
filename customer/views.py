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
            "role": user.role,
            "user_id": user.id,
            "username": user.username,
        })
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdminManagedUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


    def get_permissions(self):
        """
        Set permissions based on action.
        """
        # Admin-only actions
        if self.action in ["retrieve", "list", "destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsAdmin()]

        # Actions accessible by both admin and the user themselves
        if self.action in ["me", "change_password"]:
            return [IsAuthenticated()]

        # Default: must be authenticated
        return [IsAuthenticated()]


    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    # -------------------------
    # POST /api/users/me/change-password/
    # -------------------------
    @action(detail=False, methods=['post'], url_path='me/change-password')
    def change_password(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK
        )




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

