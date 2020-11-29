from django.db import models
from users.models import User

# Create your models here.
class Student(models.Model):
    LOCATION_CHOICES = (
        (1, "Kathmandu"),
        (2, "Pokhara"),
        (3, "Chitwan"),
        (4, "Janakpur"),
        (5, "Dang")
    )
    CULTURE_CHOICES = (
        (1, 'Brahmin'),
        (2, 'Newar'),
        (3, 'Tharu'),
        (4, 'Terai')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.PositiveIntegerField(choices=LOCATION_CHOICES)
    culture = models.PositiveIntegerField(choices=CULTURE_CHOICES)
