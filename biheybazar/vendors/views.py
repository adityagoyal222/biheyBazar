from django.shortcuts import render
from django.db.transaction import commit
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login
from django.urls.base import reverse_lazy
from django.views.generic import CreateView,ListView
from vendors.models import Vendor

# Create your views here.


class VendorList(ListView):
    '''class based view to list out all the vendors '''
    model = Vendor
    
    def get_queryset(self):      
        vendor=Vendor.objects.all()
        context = {'vendor_list':vendor}
        return super().get_queryset()