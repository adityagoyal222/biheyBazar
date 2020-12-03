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

@login_required
def give_reviews(request,pk):
    user = get_object_or_404(User,pk=pk)
    customer = get_object_or_404(Customer,pk=pk)

    vendor= get_object_or_404(Vendor,pk=7)
    
    
    if request.method == 'POST':
        form= ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = customer
            review.vendor=vendor
            review.save()
           
            
            messages.success(request, 'Review submitted')
        return redirect('vendors:reviews',pk=user.pk)

    else:
        form = ReviewForm
    return render(request,'vendors/vendor_profile.html',{'form':form,'reviews':Review.objects.all()})