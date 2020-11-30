from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import commit
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomerSignUpForm, VendorSignUpForm, UserVendorForm, UserCustomerForm
from .models import User

# Create your views here.

# View for signing up the customer
def customerSignUpView(request):
    if request.method == 'POST':

        # Two form needs to be created for signup view
        user_form = UserCustomerForm(request.POST)
        customer_form = CustomerSignUpForm(request.POST, request.FILES)

        if user_form.is_valid() and customer_form.is_valid():
            # form validation and updating models
            id = user_form.save()
            user = User.objects.get(id=id)
            customer_form.save(user)
            return HttpResponseRedirect(reverse_lazy("customers:questions"))        

        else:
            context = {
                'user_form': user_form,
                'customer_form': customer_form,
            }

    else:
        context = {
            'user_form': UserCustomerForm(),
            'customer_form': CustomerSignUpForm(),
        }

    return render(request, 'users/customer_signup.html', context)


# View for signing up vendor
def vendorSignUpView(request):
    if request.method == 'POST':
        # Two form needs to be created for signup view
        user_form = UserVendorForm(request.POST)
        vendor_form = VendorSignUpForm(request.POST, request.FILES)

        if user_form.is_valid() and vendor_form.is_valid():
            # form validation and updating models
            id = user_form.save()
            user = User.objects.get(id=id)
            vendor_form.save(user)
            return HttpResponseRedirect(reverse_lazy("vendors:detail"))        

        else:
            context = {
                'user_form': user_form,
                'vendor_form': vendor_form,
            }

    else:
        context = {
            'user_form': UserVendorForm(),
            'vendor_form': VendorSignUpForm(),
        }

    return render(request, 'users/vendor_signup.html', context)