from django.contrib import admin
from.models import Movie, Inventory, Rental
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')



class InventoryAdmin(admin.ModelAdmin):
    list_display = ('movie', 'available_copies')



class RentalAdmin(admin.ModelAdmin):
    list_display = ('movie', 'rented_at', 'status')



admin.site.register(Movie, MovieAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Rental, RentalAdmin)
