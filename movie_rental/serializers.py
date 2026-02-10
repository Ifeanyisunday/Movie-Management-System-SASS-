# serializers.py
from rest_framework import serializers
from .models import Movie, Inventory, Rental

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    available_copies = serializers.SerializerMethodField()

    def get_available_copies(self, movie):
        inventory = Inventory.objects.filter(movie=movie).first()
        return inventory.available_copies if inventory else 0


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        

class RentalSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = [
            'user',
            'status',
            'rented_at',
            'return_date'
        ]

    def validate(self, request):
        movie = request.get('movie')

        inventory = Inventory.objects.filter(movie=movie).first()
        if not inventory:
            raise serializers.ValidationError(
                "Inventory record not found for this movie."
            )

        if inventory.available_copies <= 0:
            raise serializers.ValidationError(
                "Movie is currently out of stock."
            )

        return request