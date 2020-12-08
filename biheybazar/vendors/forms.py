from django.db.models import fields
from django.forms import ModelForm
from .models import Category, Vendor
from checklist.models import VendorChecklistCategory, Checklist, ChecklistCategory
from customers.models import Customer


class UpdateLogoForm(ModelForm):
    class Meta:
        fields=('logo',)
        model = Vendor

    def __init__(self, *args, **kwargs):
        vendor_username = kwargs.pop('vendor')
        super().__init__(*args, **kwargs)
        self.vendor_object = Vendor.objects.filter(user__username=vendor_username)
    
    def save(self):
        self.vendor_object.logo = self.cleaned_data['logo']
        return self.vendor_object

class UpdateCoverImageForm(ModelForm):
    class Meta:
        fields=('cover_image',)
        model = Vendor

    def __init__(self, *args, **kwargs):
        vendor_username = kwargs.pop('vendor')
        super().__init__(*args, **kwargs)
        self.vendor_object = Vendor.objects.filter(user__username=vendor_username)
    
    def save(self):
        self.vendor_object.cover_image = self.cleaned_data['cover_image']
        return self.vendor_object

class UpdateAboutForm(ModelForm):
    class Meta:
        fields=('about',)
        model = Vendor

    def __init__(self, *args, **kwargs):
        vendor_username = kwargs.pop('vendor')
        super().__init__(*args, **kwargs)
        self.vendor_object = Vendor.objects.filter(user__username=vendor_username)
    
    def save(self):
        self.vendor_object.about = self.cleaned_data['about']
        return self.vendor_object

class AddToChecklistForm(ModelForm):
    class Meta:
        fields = ("comment", "category",)
        model = VendorChecklistCategory
    
    
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        field = []
        categories = []
        author = Customer.objects.filter(user=user)[0]
        checklist = Checklist.objects.filter(author=author)
        for i in checklist:
            field.append(self.fields['category'].queryset.filter(checklist=i))
        for i, j in enumerate(field):
            for k in j:
                categories.append(k)
        
        self.fields['category'].queryset = self.fields['category'].queryset.filter(cat_name__in=categories)
        # self.fields['category'].queryset=categories
        print('categories', categories)
        
        print('author', author)
        print('checklist', checklist)
        

    

    def save(self, vendor):
        vendor_checklist_category = VendorChecklistCategory.objects.create(
            category=self.cleaned_data['category'],
            comment=self.cleaned_data['comment'],
            vendor=vendor,
        )
        return vendor_checklist_category