from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView,
                                 DeleteView, UpdateView, ListView, FormView)
from django.views.generic.base import RedirectView
from django.contrib import messages
from users.forms import VendorSignUpForm
from reviews.forms import ReviewForm
from reviews.models import Review
from .models import Tag, Vendor, VendorTag, Category, VendorImage
from customers.models import Customer
from .forms import AddTagForm, UpdateLogoForm, UpdateAboutForm, UpdateCoverImageForm, AddImageForm, AddToChecklistForm
from django.http import HttpResponseRedirect
# Create your views here.

# TAGS
class CreateTag(LoginRequiredMixin, CreateView):
    fields = ('tag_name', 'tag_type')
    model = Tag

# CATEGORIES
class CreateCategory(LoginRequiredMixin, CreateView):
    fields = ('category_name', 'description')
    model = Category

# VendorProfile
class VendorListView(ListView):
    model = Vendor
    # context_object_name = 'vendor_list'
    def get_context_data(self,**kwargs):
        vendor = Vendor.objects.all()
        categories = Category.objects.all()
        context= super(VendorListView,self).get_context_data(**kwargs)
        context['vendor_list']=vendor
        context['categories']=categories       
        return context
    

# Category
class CreateCategory(LoginRequiredMixin, CreateView):
    fields=('category_name', 'description')
    model = Category

class VendorProfile(FormView,DetailView):
    model = Vendor
    form_class = VendorSignUpForm
    # second_form_class = ReviewForm
    # third_form_class = AddToChecklistForm
    template_name = "vendors/vendors_profile.html"
    def get_context_data(self,**kwargs):
        tags = Tag.objects.filter(vendors__user__username=self.kwargs['slug'])
        all_tags = Tag.objects.all()
        reviews= Review.objects.filter(vendor__user__username=self.kwargs['slug'])
        vendor_images = VendorImage.objects.filter(vendor__user__username=self.kwargs['slug'])
        vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
        context = super(VendorProfile, self).get_context_data(**kwargs)
        context['vendor_images'] = vendor_images
        context['tags'] = tags
        context['all_tags'] = all_tags
        context['reviews'] = reviews
        context['vendor'] = vendor
        if 'review_form' not in context:
            context['review_form'] = ReviewForm()
        if 'add_checklist_form' not in context:
            context['add_checklist_form'] = AddToChecklistForm(user=self.request.user)
        if 'update_logo_form' not in context:
            context['update_logo_form'] = UpdateLogoForm()
        if 'update_cover_form' not in context:
            context['update_cover_form'] = UpdateCoverImageForm()
        if 'update_about_form' not in context:
            context['update_about_form'] = UpdateAboutForm()
        if 'add_image_form' not in context:
            context['add_image_form'] = AddImageForm()
        if 'add_tag_form' not in context:
            context['add_tag_form'] = AddTagForm(user=self.request.user)
        return context

    # def get_form_kwargs(self,**kwargs):
    #     kwargs=super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        # kwargs['customer']=self.request.user.username
        # kwargs['vendor']=self.kwargs['slug']
        # return kwargs

    # def get_queryset(self):      
    #     reviews=Review.objects.all()
    #     context = {'reviews':reviews}
    #     return super().get_queryset()

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context={}

        if 'review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                vendor=Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                customer=Customer.objects.filter(user=self.request.user).first()
                review_form.save(vendor, customer)
            else:
                context['review_form'] = review_form
        
        elif 'add_to_checklist' in request.POST:
            add_to_checklist_form = AddToChecklistForm(request.POST, user=self.request.user)
            if add_to_checklist_form.is_valid():
                vendor=Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_to_checklist_form.save(vendor)
            else:
                context['add_to_checklist_form'] = add_to_checklist_form
        
        elif 'update_logo' in request.POST:
            update_logo_form = UpdateLogoForm(request.POST, request.FILES)
            if update_logo_form.is_valid():
                vendor=Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_logo_form.save(vendor)
            else:
                context['update_logo_form'] = update_logo_form
        
        elif 'update_cover' in request.POST:
            update_cover_form = UpdateCoverImageForm(request.POST, request.FILES)
            if update_cover_form .is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_cover_form.save(vendor)
            else:
                context['update_cover_form'] = update_cover_form
        
        elif 'update_about' in request.POST:
            update_about_form = UpdateAboutForm(request.POST)
            if update_about_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_about_form.save(vendor)
            else:
                context['update_about_form'] = update_about_form

        elif 'add_image' in request.POST:
            add_image_form = AddImageForm(request.POST, request.FILES)
            if add_image_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_image_form.save(vendor)
            else:
                context['add_image_form'] = add_image_form
        
        elif 'add_tag' in request.POST:
            add_tag_form = AddTagForm(request.POST, user=request.user)
            if add_tag_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_tag_form.save(vendor)
        return render(request, self.template_name, self.get_context_data(**context))

    # def form_valid(self,form):
    #     form.save()
    #     return HttpResponseRedirect(self.request.path_info)

