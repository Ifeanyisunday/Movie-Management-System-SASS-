# serializers.py
from rest_framework import serializers
from datetime import datetime
from .models import Movie, Inventory, Rental

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ["vendor"]
    available_copies = serializers.SerializerMethodField()

    def get_available_copies(self, movie):
        inventory = Inventory.objects.filter(movie=movie).first()
        return inventory.available_copies if inventory else 0

    def validate_release_year(self, value):
        current_year = datetime.now().year

        if value and value > current_year:
            raise serializers.ValidationError("Release year cannot be in the future.")

        if value and value < 1900:
            raise serializers.ValidationError("Release year is unrealistic.")

        return value
    


    

class InventorySerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'movie', 'movie_title', 'available_copies', 'total_copies']

    # Prevent invalid state where available copies exceed total copies
    def validate(self, data):
        total = data.get("total_copies", self.instance.total_copies)
        available = data.get("available_copies", self.instance.available_copies)

        if available > total:
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return data





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

    def validate(self, attrs):
        movie = attrs.get('movie')
        user = self.context['request'].user

        if Rental.objects.filter(
            user=user,
            movie=movie,
            status='RENTED'
        ).exists():
            raise serializers.ValidationError(
                "You already rented this movie and haven't returned it."
            )


        if not movie:
            raise serializers.ValidationError("Movie is required.")

        inventory = Inventory.objects.filter(movie=movie).first()
        if not inventory:
            raise serializers.ValidationError(
                "Inventory record not found for this movie."
            )

        if inventory.available_copies <= 0:
            raise serializers.ValidationError(
                "Movie is currently out of stock."
            )

        return attrs