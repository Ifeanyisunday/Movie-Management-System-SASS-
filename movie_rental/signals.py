from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rental, Inventory

@receiver(post_save, sender=Rental)
def update_inventory(sender, instance, created, **kwargs):
    inventory = Inventory.objects.get(movie=instance.movie)
    if created:
        inventory.available_copies -= 1
    elif instance.status == 'RETURNED':
        inventory.available_copies += 1
    inventory.save()
