'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from commercial import views

urlpatterns = patterns('',
    url(r'^webview/$', views.web_view),
    url(r'^webview/(\d+)/$', views.mobile_web_view),
    url(r'^addcomment/(\d+)/$', views.addcomment),
    url(r'^list/$', views.list_commercial),
)
