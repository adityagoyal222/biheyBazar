from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView,
                                 DeleteView, UpdateView)
from django.views.generic.base import RedirectView
from django.contrib import messages

from vendors.models import Tag, Vendor, VendorTag, Category

# Create your views here.

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
            messages.success(self.request, "You nnow have this tag")
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

# Category
class CreateCategory(LoginRequiredMixin, CreateView):
    fields=('category_name', 'description')
    model = Category

class VendorProfile(DetailView):
    model = Vendor
    template_name = "vendors/vendors_profile.html"
    def get_context_data(self,**kwargs):
        tags = Tag.objects.filter(vendors__user__username=self.kwargs['slug'])
        all_tags = Tag.objects.all()
        context = super(VendorProfile, self).get_context_data(**kwargs)
        context['tags'] = tags
        context['all_tags'] = all_tags
        return context