from django.conf.urls import url
from . import views
from reviews import views as re_view

app_name = "vendors"
urlpatterns = [
    url(r'^new/tag/$', views.CreateTag.as_view(), name="create_tag"),
    # url(r'^add/tag/$', views.AddTag.as_view(), name="add_tag"),
    # url(r'^remove/tag/$', views.RemoveTag.as_view(), name="remove_tag"),
    url(r'^new/category/$', views.CreateCategory.as_view(), name="create_category"),
    url(r'^profile/(?P<slug>[-\w]+)/$', views.VendorProfile.as_view(), name='profile'),
    url(r'^delete/image/(?P<pk>[-\w]+)/$', views.DeleteVendorImage.as_view(), name="image_delete"),
    url(r'^delete/pricing/(?P<pk>[-\w]+)/$', views.DeleteVendorPricing.as_view(), name="pricing_delete"),
    url(r'list/', views.VendorListView.as_view(), name="vendor_list"),
    url(r'venues/',views.VenueListView.as_view(),name='venues'),
    url(r'^category/(?P<pk>[-\w]+)/$',views.CategoryDetailView.as_view(),name='vendorCategory')

]