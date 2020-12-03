from django.db import models
from vendors.models import Vendor
from customers.models import Customer
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
# Create your models here.


class Review(models.Model):

    customer = models.ForeignKey(Customer,related_name="customer_review",on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,related_name="vendor_review",on_delete=models.CASCADE)
    published_date= models.DateTimeField(default=timezone.now)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    # richtextfield to give editing options in editor
    description = RichTextField(blank=True,default='',null=True)


    def __str__(self):
        return self.description

    

