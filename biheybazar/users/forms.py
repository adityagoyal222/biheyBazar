from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.transaction import commit
from django.forms import fields

from .models import User
from customers.models import Customer
from vendors.models import Vendor

class UserCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user.pk

class CustomerSignUpForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'location', 'culture')
        model = Customer

    @transaction.atomic()
    def save(self, user):
        customer = Customer.objects.create(
            user=user, 
            profile_pic=self.cleaned_data['profile_pic'])
        return customer

class UserVendorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        return user.pk


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
            user=user,
            vendor_name=self.cleaned_data['vendor_name'],
            logo=self.cleaned_data['logo'],
            cover_image=self.cleaned_data['cover_image'],
            about=self.cleaned_data['about'])
        return vendor