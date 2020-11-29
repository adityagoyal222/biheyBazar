from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import User
from ..customers.models import Customer
from ..vendors.models import Vendor

class CustomerSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'location', 'culture', 'profile_pic')
        model = get_user_model()

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.location = self.cleaned_data.get('location')
        customer.culture = self.cleaned_data.get('culture')
        customer.profile_pic = self.cleaned_data.get('profile_pic')
        return user


class VendorSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'vendor_name', 'password1', 'password2', 'logo', 'cover_image', 'about')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['vendor_name'].label = 'Vendor Name'
        self.fields['cover_image'].label = 'Cover Image'

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.vendor_name = self.cleaned_data.get('vendor_name')
        customer.logo = self.cleaned_data.get('logo')
        customer.cover_image = self.cleaned_data.get('cover_image')
        customer.about = self.cleaned_data.get('about')
        return user