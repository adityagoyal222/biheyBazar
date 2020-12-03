from django.conf.urls import url
from django.urls import path, re_path
from reviews import views as review_views
from vendors import views as vendor_views



app_name = "vendors"
urlpatterns = [
    path('',vendor_views.VendorList.as_view(),name='vendor_list'),
    re_path(r'^(?P<pk>\d+)/vendor_profile/$',review_views.give_reviews,name="reviews")
    
    
]