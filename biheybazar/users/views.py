from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView

from .forms import CustomerSignUpForm, VendorSignUpForm
from .models import User

# Create your views here.

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = "users/customer_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customers:questions')

class VendorSignUpView(CreateView):
    model = User
    form_class = VendorSignUpForm
    template_name = "users/vendor_signup.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendor'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('vendors:detail')