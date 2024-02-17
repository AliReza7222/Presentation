import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from config.models import BaseModel


class User(AbstractUser, BaseModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=258)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/avata_profile/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Profile'

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.avatar.storage.delete(str(self.avatar.name))
        return super(Profile, self).delete(*args, **kwargs)

    def __str__(self):
        return f'profile user {self.user}'
