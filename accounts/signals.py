from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        with transaction.atomic():
            Profile.objects.create(user=instance)
