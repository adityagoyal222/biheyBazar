"""biheybazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from . import views
from users import views as user_views

# Routing is defined here
# urlpatterns = [
#     path('__debug__/', include(debug_toolbar.urls)), # To use django debugger
#     path('admin/', admin.site.urls),
#     path('',views.HomePage.as_view(), name='home'),
#     url(r'^users/', include('users.urls', namespace="users")),
#     url(r'^customers/', include('customers.urls', namespace="customers")),
#     url(r'^vendors/', include('vendors.urls', namespace="vendors")),
#     url(r'^checklist/', include('checklist.urls', namespace="checklist")),
#     # path('verification/', include('verify_email.urls')),
#     # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#     #     user_views.activate, name='activate'),
#     path('activate/<uidb64>/<token>', user_views.activate, name="activate")
# ] + static(settings.MEDIA_URL,
#                          document_root=settings.MEDIA_ROOT) # To include media urls
