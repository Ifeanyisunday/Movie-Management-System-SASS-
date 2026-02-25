"""
URL configuration for SASS_MOVIE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customer.views import AnyUserViewSet, UserViewSet, AdminAnalyticsViewSet
from movie_rental.views import MovieViewSet, RentalViewSet, InventoryViewSet, HealthCheckViewSet

router = DefaultRouter()
router.register('auth', AnyUserViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('admin-analytics', AdminAnalyticsViewSet, basename='admin-analytics')
router.register('movies', MovieViewSet, basename='movies')
router.register('inventory', InventoryViewSet, basename='inventory')
router.register('rentals', RentalViewSet, basename='rentals')
router.register('health', HealthCheckViewSet, basename='health')

urlpatterns = [
    path('api/', include(router.urls)),
]

