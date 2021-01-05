from django.conf.urls import url
from . import views

app_name = "customers"
urlpatterns = [
    url(r'^questions/$', views.Questions.as_view(),name='questions'),
    url(r'^profile/(?P<pk>[-\w]+)/$', views.CustomerProfile.as_view(), name='profile')
]