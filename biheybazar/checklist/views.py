from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, request, response
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (CreateView, DetailView, DeleteView, View,
                                    UpdateView, ListView, RedirectView, FormView)
from django.contrib import messages

from .forms import CreateChecklistForm, CreateChecklistCategoryForm, CreateNoteForm, AddCollaborator
from .models import Checklist, ChecklistCategory, Note, VendorCheckCategory
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
    third_form_class = AddCollaborator
    def get_context_data(self, **kwargs):
        customers = Customer.objects.filter(user__username=self.request.user.username)
        author_checklist = Checklist.objects.filter(author__in=customers)
        checklists = Checklist.objects.all()
        checklist = Checklist.objects.get(pk=self.kwargs['pk'])
        customer_obj = Customer.objects.get(user__username=self.request.user.username)
        # print(Customer.objects.filter(user__username=self.request.user.username))
        categories = get_list_or_404(ChecklistCategory, checklist=checklist)
        context = super(ChecklistDetail, self).get_context_data(**kwargs)
        context['checklists'] = checklists
        context['checklist'] = checklist
        context['author_checklist'] = author_checklist
        context['checklist_category'] = categories
        context['notes'] = Note.objects.all()
        context['customer_obj'] = customer_obj
        if 'checklistcategory_form' not in kwargs:
            kwargs['checklistcategory_form'] = CreateChecklistCategoryForm
        if 'note_form' not in context:
            context['note_form'] = CreateNoteForm()
        if 'collaborator_form' not in context:
            context['collaborator_form'] = AddCollaborator()
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
            checklistcategory_form = CreateChecklistCategoryForm(request.POST)
            
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
        
        elif 'collaborator' in request.POST:
            collaborator_form = AddCollaborator(request.POST)

            if collaborator_form.is_valid():
                collaborator = Customer.objects.filter(user__username=collaborator_form.cleaned_data['collaborators'])[0]
                checklist = self.kwargs['pk']
                collaborator_form.save(collaborator, checklist)
            else:
                context['collaborator_form'] = collaborator_form
        
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
