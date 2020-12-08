from django.conf.urls import url, include
from . import views
from django.urls import re_path, path
from users import views as user_views

app_name = "checklist"

urlpatterns = [
    url(r'^/$', user_views.checklist_url, name="all"),
    url(r'^create/$', views.CreateChecklist.as_view(), name="checklist_create"),
    # url(r'^delete/$', views.DeleteChecklist.as_view(), name="checklist_delete"),
    re_path(r'^(?P<pk>[-\w]+)/$', views.ChecklistDetail.as_view(), name="checklist_detail"),
]