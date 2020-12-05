from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, request, response
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (CreateView, DetailView, DeleteView, View,
                                    UpdateView, ListView, RedirectView, FormView)
from django.contrib import messages

from .forms import CreateChecklistForm, CreateChecklistCategoryForm, CreateNoteForm
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
    



class ChecklistDetail(LoginRequiredMixin, DetailView, FormView):
    model = Checklist
    template_name = "checklist/checklist_detail.html"
    form_class = CreateChecklistCategoryForm
    second_form_class = CreateNoteForm
    def get_context_data(self, **kwargs):
        customer = Customer.objects.filter(user=self.request.user)
        author_checklist = Checklist.objects.filter(author__in=customer)
        checklists = Checklist.objects.all()
        checklist = Checklist.objects.filter(pk=self.kwargs['pk'])[0]
        categories = get_list_or_404(ChecklistCategory, checklist=checklist)
        category = self.request.POST.get('category_pk')
        context = super(ChecklistDetail, self).get_context_data(**kwargs)
        context['checklists'] = checklists
        context['checklist'] = checklist
        context['author_checklist'] = author_checklist
        context['checklist_category'] = categories
        if 'checklistcategory_form' not in kwargs:
            kwargs['checklistcategory_form'] = CreateChecklistCategoryForm
        if 'note_form' not in context:
            context['note_form'] = CreateNoteForm()
        return context
    
    # def get_form_kwargs(self, **kwargs):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['checklist'] = self.kwargs['pk']
    #     kwargs['template_category'] = 1
    #     return kwargs

    # def form_valid(self, form):
    #     if 'form' in self.request.POST:
    #         form.save(self.checklist)
    #     else:
    #         print(form.cleaned_data['text'])
    #         form.save(self.category)
    #     return HttpResponseRedirect(self.request.path_info)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}

        if 'checklist_category' in request.POST:
            checklistcategory_form = CreateChecklistCategoryForm(request.POST, use_required_attribute=False)
            
            if checklistcategory_form.is_valid():
                checklistcategory_form.save(Checklist.objects.filter(pk=self.kwargs['pk'])[0])
            else:
                context['form'] = checklistcategory_form
        
        elif 'note' in request.POST:
            note_form = CreateNoteForm(request.POST)

            if note_form.is_valid():
                category = ChecklistCategory.objects.filter(pk=self.request.POST.get('category_pk'))[0]
                note_form.save(category)
            else:
                context['note_form'] = note_form
        
        return render(request, self.template_name, self.get_context_data(**context))


# class CreateCategory(LoginRequiredMixin, CreateView):
#     model = ChecklistCategory
#     form_class = CreateChecklistCategoryForm
#     template_name = "checklist/checklist_detail.html"

#     def get_form_kwargs(self, **kwargs):
#         kwargs = super().get_form_kwargs()
#         kwargs['checklist'] = self.kwargs['pk']
#         return kwargs

    # def get_context_data(self, **kwargs):
    #     category_form =  self.form_class
    #     context = super(CreateCategory, self).get_context_data(**kwargs)
    #     context['category_form'] = category_form
    #     return context
