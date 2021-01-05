from django.views.generic import (TemplateView, ListView)
from vendors.models import Vendor, Category
class HomePage(TemplateView):
    template_name='users\index.html'


    def get_context_data(self,**kwargs):
        ordered_vendor = Vendor.objects.all().order_by('-review_int')[:5]
        categories = Category.objects.all()
        print(ordered_vendor)
        context= super(HomePage,self).get_context_data(**kwargs)
        context['ordered_vendor'] = ordered_vendor 
        context['categories']=categories   
        return context