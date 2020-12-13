from django.conf.urls import url, include
from . import views
from django.urls import re_path, path
from users import views as user_views

app_name = "checklist"

urlpatterns = [
    url(r'^$', user_views.checklist_url, name="all"),
    url(r'^create/$', views.CreateChecklist.as_view(), name="checklist_create"),
    re_path(r'^(?P<pk>[-\w]+)/$', views.ChecklistDetail.as_view(), name="checklist_detail"),
    url(r'^delete/note/(?P<pk>[-\w]+)/$', views.DeleteNote.as_view(), name="note_delete"),
    url(r'^delete/category/(?P<pk>[-\w]+)/$', views.DeleteChecklistCategory.as_view(), name="checklistcategory_delete"),
    url(r'^remove/vendor/(?P<pk>[-\w]+)/$', views.RemoveChecklistVendor.as_view(), name="vendor_remove"),
    url(r'^delete/checklist/(?P<pk>[-\w]+)/$', views.DeleteChecklist.as_view(), name="checklist_delete"),
    url(r'^remove/collaborator/(?P<pk>[-\w]+)/$', views.removeCollaborator, name='collaborator_remove'),
]