from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.transaction import commit
from django.forms import fields
from ckeditor.fields import RichTextField
from .models import User
from customers.models import Customer
from vendors.models import Vendor


# Form for registering user instance in the database for customer signup
class UserCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    # @transaction.atomic() # makes the transaction atomic. i.e. all or none
    # def save(self, commit):
    #     user = super().save(commit=False)
    #     user.is_customer = True # determines that the user will registered as customer
    #     user.save(commit=commit)
    #     return user.pk


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

        # widgets={
        #     'about':forms.Textarea(attrs={ 'class':"editable medium-editor-textarea"})
        #     }
    
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
        exclude=('user', 'slug')
        model = Vendor


        widgets={
            'about':forms.Textarea(attrs={ 'class':"about-text"})
            }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor_name'].label = 'Vendor Name'
        self.fields['cover_image'].label = 'Cover Image'
        # self.fields['category'].label = 'Categories'
        self.fields['category'].label = 'Category'
        self.fields['about'].label=''

    @transaction.atomic()
    def save(self, user):
        vendor = Vendor.objects.create(
            user=user, # foreign key -> user object
            vendor_name=self.cleaned_data['vendor_name'],
            logo=self.cleaned_data['logo'],
            cover_image=self.cleaned_data['cover_image'],
            about=self.cleaned_data['about'],
            category=self.cleaned_data['category'],
            slug=user.username)
        return vendor