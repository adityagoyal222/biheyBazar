from enum import unique
from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from users.models import User
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('home')

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    vendor_name = models.CharField(max_length=200, blank=False)
    logo = models.ImageField(upload_to='logo')
    cover_image = models.ImageField(upload_to='cover_image')
    slug = models.SlugField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    about = RichTextField(blank=True,default='',null=True)
    # String representation of vendor model
    def __str__(self):
        return self.vendor_name

class VendorImage(models.Model):
    # Model for uploading images to a vendor account
    vendor = models.ForeignKey(Vendor, on_delete=CASCADE, related_name='images')
    image = models.ImageField(upload_to='vendor_images')


class Tag(models.Model):
    tag_name = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    vendors = models.ManyToManyField(Vendor, through="VendorTag", related_name="vendor_tag")

    def __str__(self):
        return self.tag_name
    
    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['tag_name']

class VendorTag(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="vendor_tags", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name="vendor", on_delete=models.CASCADE)

    def __str__(self):
        return self.vendor.vendor_name

    class Meta:
        unique_together = ('vendor', 'tag')