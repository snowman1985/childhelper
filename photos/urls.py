from django.conf.urls import patterns, include, url

from django.contrib import admin
from photos.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^uploadhead/', upload_head),
    url(r'^gethead/', get_head),
)
