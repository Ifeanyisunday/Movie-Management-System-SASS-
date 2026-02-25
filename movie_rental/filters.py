import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):

    # Exact genre filter
    genre = django_filters.CharFilter(field_name="genre", lookup_expr="iexact")

    # Price range filters
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )

    class Meta:
        model = Movie
        fields = ['genre', 'min_price', 'max_price']
