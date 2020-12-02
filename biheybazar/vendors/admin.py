from django.contrib import admin
from vendors.models import Vendor, VendorImage, Tag, Categories, VendorTag
# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorImage)
admin.site.register(VendorTag)
admin.site.register(Tag)
admin.site.register(Categories)