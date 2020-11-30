from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import commit
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView


from .forms import CustomerSignUpForm, VendorSignUpForm, UserVendorForm, UserCustomerForm
from .models import User

# Create your views here.

# class CustomerSignUpView(CreateView):
#     model = User
#     template_name = "users/customer_signup.html"
#     form_class=UserCustomerForm

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'customer'
#         return super().get_context_data(**kwargs)
    
#     def post(self, request, *args, **kwargs):
#         if request.POST():
#             a_valid = UserCustomerForm.is_valid()
#             b_valid = CustomerSignUpForm.is_valid()
#             c_valid = UserVendorForm.is_valid()
#             d_valid = VendorSignUpForm.is_valid()

#             if a_valid and b_valid and c_valid and d_valid:
#                 a = UserCustomerForm.save()
#                 b = CustomerSignUpForm.save(a)
#                 c = UserVendorForm.save()
#                 d = VendorSignUpForm.save(c)

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('customers:questions')

# class VendorSignUpView(CreateView):
#     model = User
#     form_class = VendorSignUpForm
#     template_name = "users/vendor_signup.html"

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'vendor'
#         return super().get_context_data(**kwargs)
    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('vendors:detail')

def customerSignUpView(request):
    if request.method == 'POST':

        user_form = UserCustomerForm(request.POST)
        customer_form = CustomerSignUpForm(request.POST, request.FILES)

        if user_form.is_valid() and customer_form.is_valid():

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

def vendorSignUpView(request):
    if request.method == 'POST':

        user_form = UserVendorForm(request.POST)
        vendor_form = VendorSignUpForm(request.POST, request.FILES)

        if user_form.is_valid() and vendor_form.is_valid():

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