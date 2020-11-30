from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.transaction import commit
from django.forms import fields

from .models import User
from customers.models import Customer
from vendors.models import Vendor


# Form for registering user instance in the database for customer signup
class UserCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    @transaction.atomic() # makes the transaction atomic. i.e. all or none
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True # determines that the user will registered as customer
        user.save()
        return user.pk


# Form for registering customer instance in the database for customer signup
class CustomerSignUpForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'location', 'culture')
        model = Customer

    @transaction.atomic()
    def save(self, user):
        customer = Customer.objects.create(
            user=user, # foreign key -> user object
            profile_pic=self.cleaned_data['profile_pic'])
        return customer

# Form for registering user instance in the database for vendor signup
class UserVendorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True # determines that the user will registered as vendor
        user.save()
        return user.pk


# Form for registering vendor instance in the database for vendor signup
class VendorSignUpForm(forms.ModelForm):
    user = UserVendorForm()
    class Meta:
        exclude=('user',)
        model = Vendor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor_name'].label = 'Vendor Name'
        self.fields['cover_image'].label = 'Cover Image'

    @transaction.atomic()
    def save(self, user):
        vendor = Vendor.objects.create(
            user=user, # foreign key -> user object
            vendor_name=self.cleaned_data['vendor_name'],
            logo=self.cleaned_data['logo'],
            cover_image=self.cleaned_data['cover_image'],
            about=self.cleaned_data['about'])
        return vendor