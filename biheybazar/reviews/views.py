from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from vendors.models import Vendor
from customers.models import Customer
from users.models import User
from reviews.forms import ReviewForm
from django.contrib import messages
from reviews.models import Review

# Create your views here.

#==================================reviews-ratings view==============================================#

#====== in progress, might have to use CBVs =========#

# @login_required
# def give_reviews(request,slug):
#     print("hello")
#     template_name = "vendors/vendors_profile.html"
#     user = get_object_or_404(User,pk=request.user.pk)
#     customer = get_object_or_404(Customer,user=user)

#     vendor= get_object_or_404(Vendor,slug=slug)
    
#     if request.method == 'POST':
#         form= ReviewForm(request.POST)
        
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.customer = customer
#             review.vendor=vendor
#             review.save()
           
            
#             messages.success(request, 'Review submitted')
#         return redirect('vendors:profile',pk=user.pk)

#     else:
       
#         form = ReviewForm()
#     return render(request,'vendors/vendors_profile.html',{ 'form':form,'reviews':Review.objects.all()})