from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (CreateView, DetailView, DeleteView,
                                    UpdateView, ListView, RedirectView)
from django.contrib import messages

from .forms import CreateChecklistForm, CreateChecklistCategoryForm
from .models import Checklist, ChecklistCategory, Note, Collaborators, VendorCheckCategory
from customers.models import Customer

# Create your views here.

class CreateChecklist(LoginRequiredMixin, CreateView):
    form_class = CreateChecklistForm
    template_name = "checklist/create_checklist.html"
    model = Checklist
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    

class ChecklistDetail(LoginRequiredMixin, DetailView):
    model = Checklist
    template_name = "checklist/checklist_detail.html"

    def get_context_data(self, **kwargs):
        customer = Customer.objects.filter(user=self.request.user)
        author_checklist = Checklist.objects.filter(author__in=customer)
        checklists = Checklist.objects.all()
        checklist = Checklist.objects.filter(pk=self.kwargs['pk'])[0]
        context = super(ChecklistDetail, self).get_context_data(**kwargs)
        context['checklists'] = checklists
        context['checklist'] = checklist
        context['author_checklist'] = author_checklist
        context['category_form'] = CreateChecklistCategoryForm
        return context
    
    # def get_form_kwargs(self, **kwargs):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['checklist'] = self.kwargs['pk']
    #     return kwargs


class CreateCategory(LoginRequiredMixin, CreateView):
    model = ChecklistCategory
    form_class = CreateChecklistCategoryForm
    template_name = "checklist/create_checklist_category.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['checklist'] = self.kwargs['pk']
        return kwargs

    # def get_context_data(self, **kwargs):
    #     category_form =  self.form_class
    #     context = super(CreateCategory, self).get_context_data(**kwargs)
    #     context['category_form'] = category_form
    #     return context