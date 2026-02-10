from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnyUserViewSet

# router = DefaultRouter()
# router.register(r'users', AnyUserViewSet, basename='users')

# urlpatterns = [
#     path('', include(router.urls)),
# ]