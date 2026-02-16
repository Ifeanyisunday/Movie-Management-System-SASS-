from django.db import models
from SASS_MOVIE import settings
from django.core.validators import MinValueValidator
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Inventory(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    available_copies = models.PositiveIntegerField(
    validators=[MinValueValidator(0)]
)

    def __str__(self):
        return f"{self.movie.title} - {self.available_copies}"


class Rental(models.Model):
    STATUS_CHOICES = (
        ('RENTED', 'Rented'),
        ('RETURNED', 'Returned'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rented_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="RENTED"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                condition=Q(status='RENTED'),
                name='unique_active_rental'
            )
        ]

    def __str__(self):
        return f"{self.movie} - {self.status}"
