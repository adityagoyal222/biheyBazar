from django.contrib import admin
from .models import Checklist, ChecklistCategory, Note, VendorCheckCategory

# Register your models here.
admin.site.register(Checklist)
admin.site.register(ChecklistCategory)
admin.site.register(Note)
# admin.site.register(Collaborators)
admin.site.register(VendorCheckCategory)