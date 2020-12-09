from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import commit
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from verify_email.email_handler import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage


from .forms import CustomerSignUpForm, VendorSignUpForm, UserVendorForm, UserCustomerForm
from .models import User
from customers.models import Customer
from checklist.models import Checklist

from .tokens import account_activation_token


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
            user = user_form.save(commit=False)
            user.is_customer = True
            user.save()
            user_obj = User.objects.get(username=user_form.cleaned_data['username'])
            customer_form.save(user_obj)
            # inactive_user = send_verification_email(request, user_form)
            # print(user_form.cleaned_data['email'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate you BiheyBazar account'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
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
            user = user_form.save(commit=False)
            user.is_vendor=True
            user.save()
            user_obj = User.objects.get(username=user_form.cleaned_data['username'])
            vendor_form.save(user_obj)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your BiheyBazar account'
            message = render_to_string('users/acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponseRedirect(reverse_lazy("users:login"))        

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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponseRedirect(reverse_lazy("users:login"))
    else:
        return HttpResponse('Activation link is invalid')


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


def checklist_url(request):
    author_checklists = Checklist.objects.filter(author__user=request.user)
    shared_checklists = Checklist.objects.filter(collaborators__user=request.user)
    if author_checklists:
        pk = author_checklists.first().pk
        return redirect("checklist:checklist_detail", pk=pk)
    else:
        if shared_checklists:
            pk = shared_checklists.first().pk
            return redirect("checklist:checklist_detail", pk=pk)
        else:
            return redirect("checklist:checklist_create")