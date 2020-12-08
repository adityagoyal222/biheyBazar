from django.contrib import admin
from vendors.models import Vendor, VendorImage, Tag, VendorTag, Category

# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorImage)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(VendorTag)
