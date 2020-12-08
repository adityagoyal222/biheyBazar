from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import commit
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView


from .forms import CustomerSignUpForm, VendorSignUpForm, UserVendorForm, UserCustomerForm
from .models import User
from customers.models import Customer
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
            return HttpResponseRedirect(reverse_lazy("users:login"))        

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
            return HttpResponseRedirect(reverse_lazy("vendors:profile", kwargs={'slug':user.username}))        

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



# function view to check the type of user and redirct them accordingly,
def userCheckView(request):
    user = request.user

    #if user is vendor s/he should be redirected to their respective profile
    if user.is_vendor:
        return redirect('vendors:profile', slug=user)

    #if user is customer redirect them to either questions page or home page    
    elif user.is_customer:
        customer=Customer.objects.get(user=user)
        if customer.location==None or customer.culture==None:
            return HttpResponseRedirect(reverse_lazy("customers:questions"))

        else:
            return HttpResponseRedirect(reverse_lazy("home"))
    else:
        return HttpResponseRedirect(reverse_lazy("home"))