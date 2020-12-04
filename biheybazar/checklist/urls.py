from django.conf.urls import url, include
from . import views

app_name = "checklist"

urlpatterns = [
    url(r'^create/$', views.CreateChecklist.as_view(), name="checklist_create"),
    # url(r'^delete/$', views.DeleteChecklist.as_view(), name="checklist_delete"),
    url(r'^(?P<pk>[-\w]+)/$', views.ChecklistDetail.as_view(), name="checklist_detail"),
]