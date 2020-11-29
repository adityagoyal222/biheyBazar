from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Creates an AbstractUser called User for authentication 
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username