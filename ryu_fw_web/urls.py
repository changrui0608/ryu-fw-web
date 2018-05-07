"""ryu_fw_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # index page
    url(r'^$', views.index, name='index'),

    # settings and status
    url(r'^status/$', views.status, name='status'),
    url(r'^status/enable/$', views.status_enable, name='status_enable_all'),
    url(r'^status/enable/(?P<sw>[0-9]+)/$', views.status_enable, name='status_enable'),
    url(r'^status/disable/$', views.status_disable, name='status_disable_all'),
    url(r'^status/disable/(?P<sw>[0-9]+)/$', views.status_disable, name='status_disable'),
    
    
    # all -- show all detailed rules

    # IP / IP range -- a quick entry for set rules based on IP / IP range

    
]
