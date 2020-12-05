from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from .models import Checklist, ChecklistCategory, Note
from customers.models import Customer

class CreateChecklistForm(ModelForm):
    class Meta:
        exclude=('author', "can_edit", "checklist_collaborators")
        model = Checklist

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.customer_object = Customer.objects.filter(user=user)[0]

    def save(self):
        checklist = Checklist.objects.create(
            checklist_name=self.cleaned_data['checklist_name'], # foreign key -> user object
            description=self.cleaned_data['description'],
            author=self.customer_object,
            can_edit=True)
        return checklist

    
class CreateChecklistCategoryForm(ModelForm):
    class Meta:
        fields = ("cat_name",)
        model = ChecklistCategory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat_name'].label = "Category Name"

    def save(self, checklist):
        checklist_category = ChecklistCategory.objects.create(
            cat_name=self.cleaned_data['cat_name'],
            checklist = checklist
        )
        return checklist_category

class CreateNoteForm(ModelForm):
    class Meta:
        fields = ("text",)
        model = Note

    # def __init__(self, *args, **kwargs):
    #     category = kwargs.pop('template_category')
    #     print(category)
    #     super().__init__(*args, **kwargs)
    #     self.category = get_object_or_404(ChecklistCategory, pk=category)
    
    def save(self, category):
        note = Note.objects.create(
            text=self.cleaned_data['text'],
            category = category
        )
        return note