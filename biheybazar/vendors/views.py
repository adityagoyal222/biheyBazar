from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView,
                                 DeleteView, UpdateView, ListView, FormView)
from django.views.generic.base import RedirectView
from django.contrib import messages
from users.forms import VendorSignUpForm
from reviews.forms import ReviewForm
from reviews.models import Review
from .models import Tag, Vendor, VendorPricing, VendorTag, Category, VendorImage
from customers.models import Customer
from .forms import (AddTagForm, UpdateLogoForm,
                 UpdateAboutForm, UpdateCoverImageForm,
                  AddImageForm, AddToChecklistForm,
                  UpdateAddressForm, UpdateContactForm,
                  AddPricingForm)
from django.http import HttpResponseRedirect
# Create your views here.

# TAGS





class CreateTag(LoginRequiredMixin, CreateView):
    fields = ('tag_name', 'tag_type')
    model = Tag

# CATEGORIES
class CreateCategory(LoginRequiredMixin, CreateView):
    fields = ('category_name', 'description', 'category_pic')
    model = Category

# VendorProfile
class VendorListView(ListView):
    model = Vendor
    # template_name = 'users/index.html'
    # context_object_name = 'vendor_list'
    def get_context_data(self,**kwargs):
        vendor = Vendor.objects.all().order_by('-review_int')[:6]
        categories = Category.objects.all()
        context= super(VendorListView,self).get_context_data(**kwargs)
        context['vendor_list']=vendor
        context['categories']=categories
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'vendors/categoryDetail.html'

    def get_context_data(self,**kwargs):
        # self.request.session['vendor_slug'] = self.kwargs['slug']
        categories= Category.objects.filter(pk=self.kwargs['pk']).first()
        vendor= Vendor.objects.filter(category=categories)
        print(categories)
        context= super(CategoryDetailView,self).get_context_data(**kwargs)
        context['vendor_list']=vendor
        context['categories']=categories
        return context

# Category
class CreateCategory(LoginRequiredMixin, CreateView):
    fields=('category_name', 'description')
    model = Category

class VenueListView(ListView):
    model = Vendor
    template_name = "vendors/venues.html"



    # context_object_name = 'vendor_list'
    def get_context_data(self,**kwargs):
        # vendor = Vendor.objects.filter(Vendor.category)
        # print(vendor)
        # for v in vendor:
        #     print(v.category)
        # categories = Category.objects.all()
        # for v in categories:
        #     print(v.vendor_name)

        vendor=Vendor.objects.all()
        print(vendor)
        for v in vendor:
            print(v.category)
        context= super(VenueListView,self).get_context_data(**kwargs)
        context['venues']=vendor
        # context['categories']=categories
        return context


class DeleteVendorImage(LoginRequiredMixin, DeleteView):
    model = VendorImage

    def get_success_url(self):
        return reverse_lazy('vendors:profile', kwargs={'slug':self.request.session.get('vendor_slug')})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DeleteVendorPricing(LoginRequiredMixin, DeleteView):
    model = VendorPricing

    def get_success_url(self):
        return reverse_lazy('vendors:profile', kwargs={'slug':self.request.session.get('vendor_slug')})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VendorProfile(FormView,DetailView):
    model = Vendor
    form_class = VendorSignUpForm
    # second_form_class = ReviewForm
    # third_form_class = AddToChecklistForm
    template_name = "vendors/vendors_profile.html"
    def get_context_data(self,**kwargs):
        self.request.session['vendor_slug'] = self.kwargs['slug']
        tags = Tag.objects.filter(vendors__user__username=self.kwargs['slug'])
        all_tags = Tag.objects.all()
        reviews= Review.objects.filter(vendor__user__username=self.kwargs['slug'])
        vendor_images = VendorImage.objects.filter(vendor__user__username=self.kwargs['slug'])
        vendor_pricing = VendorPricing.objects.filter(vendor__user__username=self.kwargs['slug'])
        vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
        vendor.avg_ratings()
        # vendor.order_vendor()
        # vendor.avg_ratings()
        # print(rt)
        context = super(VendorProfile, self).get_context_data(**kwargs)
        context['vendor_images'] = vendor_images
        context['vendor_pricing'] = vendor_pricing
        context['tags'] = tags
        context['all_tags'] = all_tags
        context['reviews'] = reviews
        context['vendor'] = vendor
        # context['avg_ratings']= vendor.avg_ratings()
        if 'rate-form' not in context:
            context['rate-form'] = ReviewForm()
        if 'add_checklist_form' not in context:
            context['add_checklist_form'] = AddToChecklistForm(user=self.request.user)
        if 'update_logo_form' not in context:
            context['update_logo_form'] = UpdateLogoForm()
        if 'update_cover_form' not in context:
            context['update_cover_form'] = UpdateCoverImageForm()
        if 'update_about_form' not in context:
            context['update_about_form'] = UpdateAboutForm()
        if 'update_address_form' not in context:
            context['update_address_form'] = UpdateAddressForm()
        if 'update_contact_form' not in context:
            context['update_contact_form'] = UpdateContactForm()
        if 'add_image_form' not in context:
            context['add_image_form'] = AddImageForm()
        if 'add_pricing_form' not in context:
            context['add_pricing_form'] = AddPricingForm()
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

        if 'ratings' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                vendor=Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                customer=Customer.objects.filter(user=self.request.user).first()
                review_form.save(vendor, customer)
            else:
                context['rate-form'] = review_form

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

        elif 'update_address' in request.POST:
            update_address_form = UpdateAddressForm(request.POST)
            if update_address_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_address_form.save(vendor)
            else:
                context['update_address_form'] = update_address_form

        elif 'update_contact' in request.POST:
            update_contact_form = UpdateContactForm(request.POST)
            if update_contact_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_contact_form.save(vendor)
            else:
                context['update_contact_form'] = update_contact_form

        elif 'add_image' in request.POST:
            add_image_form = AddImageForm(request.POST, request.FILES)
            if add_image_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_image_form.save(vendor)
            else:
                context['add_image_form'] = add_image_form

        elif 'add_pricing' in request.POST:
            add_pricing_form = AddPricingForm(request.POST, request.FILES)
            if add_pricing_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_pricing_form.save(vendor)
            else:
                context['add_pricing_form'] = add_pricing_form

        elif 'add_tag' in request.POST:
            add_tag_form = AddTagForm(request.POST, user=request.user)
            if add_tag_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                add_tag_form.save(vendor)
        return render(request, self.template_name, self.get_context_data(**context))

    # def form_valid(self,form):
    #     form.save()
    #     return HttpResponseRedirect(self.request.path_info)

