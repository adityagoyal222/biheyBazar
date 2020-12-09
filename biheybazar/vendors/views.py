from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView,
                                 DeleteView, UpdateView, ListView, FormView)
from django.views.generic.base import RedirectView
from django.contrib import messages
from users.forms import VendorSignUpForm
from .forms import AddToChecklistForm
from reviews.forms import ReviewForm
from reviews.models import Review
from vendors.models import Tag, Vendor, VendorTag, Category
from customers.models import Customer
from .forms import UpdateLogoForm, UpdateAboutForm, UpdateCoverImageForm
from django.http import HttpResponseRedirect
# Create your views here.

# TAGS
class CreateTag(LoginRequiredMixin, CreateView):
    fields = ('tag_name', 'description')
    model = Tag

class AddTag(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('vendors:profile', kwargs={'slug':self.request.user.username})
    
    def get(self, *args, **kwargs):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))

        try:
            VendorTag.objects.create(vendor=self.request.user, tag=tag)
        except:
            messages.warning(self.request, 'You already have this tag')
        else:
            messages.success(self.request, "You now have this tag")
        return super().get(self.request, *args, **kwargs)

class RemoveTag(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('vendors:profile', kwargs={'slug':self.request.user.username})

    def get(self, *args, **kwargs):
        
        try:
            vendortag = VendorTag.objects.filter(
                vendor__user = self.request.user,
                tag__pk = self.kwargs.get('pk')
            ).get()
        except VendorTag.DoesNotExist:
            messages.warning(self.request, "You do not have this tag")
        else:
            vendortag.delete()
            messages.success(self.request, "The tag was removed from your profile")
        return super().get(self.request, *args, **kwargs)

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
        vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
        context = super(VendorProfile, self).get_context_data(**kwargs)
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
        
        elif 'update_logo_form' in request.POST:
            update_logo_form = UpdateLogoForm(request.POST, request.FILES)
            if update_logo_form.is_valid():
                vendor=Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_logo_form.save(vendor)
            else:
                context['update_logo_form'] = update_logo_form
        
        elif 'update_cover_form' in request.POST:
            update_cover_form = UpdateCoverImageForm(request.POST, request.FILES)
            if update_cover_form .is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_cover_form.save(vendor)
            else:
                context['update_cover_form'] = update_cover_form
        
        elif 'update_about_form' in request.POST:
            update_about_form = UpdateAboutForm(request.POST)
            if update_about_form.is_valid():
                vendor = Vendor.objects.filter(user__username=self.kwargs['slug']).first()
                update_about_form.save(vendor)
            else:
                context['update_about_form'] = update_about_form


        return render(request, self.template_name, self.get_context_data(**context))

    # def form_valid(self,form):
    #     form.save()
    #     return HttpResponseRedirect(self.request.path_info)


class UpdateLogo(UpdateView):
    model = Vendor
    template_name = "vendors/vendor_profile.html"
    form_class = UpdateLogoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.kwargs['slug']

class UpdateCoverImage(UpdateView):
    model = Vendor
    template_name = "vendors/vendor_profile.html"
    form_class = UpdateCoverImageForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.kwargs['slug']

class UpdateAbout(UpdateView):
    model = Vendor
    template_name = "vendors/vendor_profile.html"
    form_class = UpdateAboutForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.kwargs['slug']
