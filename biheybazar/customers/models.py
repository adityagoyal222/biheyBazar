from django.db import models
from users.models import User

# Create your models here.
class Customer(models.Model):

    # ENUM field for location choices (user can choose between one of them)
    LOCATION_CHOICES = (
        (1, "Kathmandu"),
        (2, "Pokhara"),
        (3, "Chitwan"),
        (4, "Janakpur"),
        (5, "Dang")
    )
    # ENUM field for culture choices (user can choose between one of them)
    CULTURE_CHOICES = (
        (1, 'Brahmin'),
        (2, 'Newar'),
        (3, 'Tharu'),
        (4, 'Terai')
    )

    # A One-to-one Relationship between user and customer.
    # Allows addition of fields which are only specific to Customers
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.PositiveIntegerField(choices=LOCATION_CHOICES)
    culture = models.PositiveIntegerField(choices=CULTURE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pic')
