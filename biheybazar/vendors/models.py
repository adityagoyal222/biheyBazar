from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

#Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    vendor_name = models.CharField(max_length=200, blank=False)
    logo = models.ImageField(upload_to='logo')
    cover_image = models.ImageField(upload_to='cover_image')
    about = models.TextField()

class VendorImage(models.Model):
    # Model for uploading images to a vendor account
    vendor = models.ForeignKey(Vendor, on_delete=CASCADE, related_name='images')
    image = models.ImageField(upload_to = 'vendor_media')