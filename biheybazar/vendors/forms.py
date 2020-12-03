from django.forms import ModelForm
from .models import Vendor


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
