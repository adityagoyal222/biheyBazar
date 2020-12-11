from django.db.models import fields
from django.db.models.fields.files import ImageField
from django.forms import ModelForm
from .models import Category, Vendor, VendorImage, VendorTag, Tag
from checklist.models import VendorChecklistCategory, Checklist, ChecklistCategory
from customers.models import Customer


class UpdateLogoForm(ModelForm):
    class Meta:
        fields=('logo',)
        model = Vendor

    # def __init__(self, *args, **kwargs):
    #     vendor_username = kwargs.pop('vendor')
    #     super().__init__(*args, **kwargs)
    #     self.vendor_object = Vendor.objects.filter(user__username=vendor_username)
    
    def save(self, vendor):
        vendor.logo = self.cleaned_data['logo']
        vendor.save()
        return vendor

class UpdateCoverImageForm(ModelForm):
    class Meta:
        fields=('cover_image',)
        model = Vendor

    # def __init__(self, *args, **kwargs):
    #     vendor_username = kwargs.pop('vendor')
    #     super().__init__(*args, **kwargs)
    #     self.vendor_object = Vendor.objects.filter(user__username=vendor_username)
    
    def save(self, vendor):
        vendor.cover_image = self.cleaned_data['cover_image']
        vendor.save()
        return vendor

class UpdateAboutForm(ModelForm):
    class Meta:
        fields=('about',)
        model = Vendor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about'].label = ''
    
    def save(self, vendor):
        vendor.about = self.cleaned_data['about']
        vendor.save()
        return vendor

class AddImageForm(ModelForm):
    class Meta:
        fields=('image',)
        model = VendorImage

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = ''
    
    def save(self, vendor):
        vendor_image = VendorImage.objects.create(
            vendor = vendor,
            image = self.cleaned_data['image'],
        )
        return vendor_image


class AddTagForm(ModelForm):
    class Meta:
        fields=('tag',)
        model = VendorTag

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        field=[]
        tags=[]
        vendor = Vendor.objects.filter(user=user).first()
        tag = Tag.objects.filter(vendors=vendor)
        for i in tag:
            field.append(self.fields['tag'].queryset.filter(tag_name=i))
        for i, j in enumerate(field):
            for k in j:
                tags.append(k)
        self.fields['tag'].queryset = self.fields['tag'].queryset.exclude(tag_name__in=tags)

    def save(self, vendor):
        vendor_tag = VendorTag.objects.create(
            tag=self.cleaned_data['tag'],
            vendor=vendor,
        )
        return vendor_tag

class AddToChecklistForm(ModelForm):
    class Meta:
        fields = ("comment", "category",)
        model = VendorChecklistCategory
    
    
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        field = []
        categories = []
        author = Customer.objects.filter(user=user).first()
        checklist = Checklist.objects.filter(author=author)
        for i in checklist:
            field.append(self.fields['category'].queryset.filter(checklist=i))
        for i, j in enumerate(field):
            for k in j:
                categories.append(k)
        
        self.fields['category'].queryset = self.fields['category'].queryset.filter(cat_name__in=categories)

    

    def save(self, vendor):
        vendor_checklist_category = VendorChecklistCategory.objects.create(
            category=self.cleaned_data['category'],
            comment=self.cleaned_data['comment'],
            vendor=vendor,
        )
        return vendor_checklist_category