from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Creates an AbstractUser called User for authentication 
class User(AbstractUser):
    # Boolean Fields for determining user types
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    # String representation of the User model
    def __str__(self):
        return self.username