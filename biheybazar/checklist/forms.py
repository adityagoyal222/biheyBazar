from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import Checklist, ChecklistCategory
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
        checklist = kwargs.pop('checklist')
        super().__init__(*args, **kwargs)
        self.checklist = Checklist.objects.filter(pk=checklist)[0]

    def save(self):
        checklist_category = ChecklistCategory.objects.create(
            cat_name=self.cleaned_data['cat_name'],
            checklist = self.checklist
        )
        return checklist_category
