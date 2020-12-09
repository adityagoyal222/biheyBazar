from django.db import models
from customers.models import Customer
from vendors.models import Vendor
from django.urls import reverse

# Create your models here.
class Checklist(models.Model):
    checklist_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="author")
    can_edit = models.BooleanField(default=True)
    collaborators = models.ManyToManyField(Customer, blank=True)

    def __str__(self):
        return self.checklist_name
    
    def get_absolute_url(self):
        return reverse('checklist:checklist_detail', kwargs={'pk': self.pk})

class ChecklistCategory(models.Model):
    cat_name = models.CharField(max_length=100)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="checklist")
    vendors = models.ManyToManyField(Vendor, through='VendorChecklistCategory', blank=True)

    def __str__(self):
        return self.cat_name

class Note(models.Model):
    text = models.CharField(max_length=300)
    category = models.ForeignKey(ChecklistCategory, on_delete=models.CASCADE, related_name="category_note")

    def __str__(self):
        return self.text

# class Collaborators(models.Model):
#     checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
#     collaborator = models.ForeignKey(Customer, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.checklist.checklist_name

class VendorChecklistCategory(models.Model):
    category = models.ForeignKey(ChecklistCategory, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.comment