from django.conf.urls import url
from vendors import views

app_name = "vendors"
urlpatterns = [
    url(r'^new/tag/$', views.CreateTag.as_view(), name="create_tag"),
    url(r'^add/tag/$', views.AddTag.as_view(), name="add_tag"),
    url(r'^remove/tag/$', views.RemoveTag.as_view(), name="remove_tag"),
    url(r'^new/category/$', views.CreateCategory.as_view(), name="create_category"),
    url(r'^profile/(?P<slug>[-\w]+)/$', views.VendorProfile.as_view(), name='profile'),
]