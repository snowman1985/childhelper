'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^topic/webview/(\d+)/(\d+)/$', topic_webview, name='topic_webview'),
    url(r'^addcommentwebview/(\d+)/(\d+)/$', addcommentwebview, name='addcommentwebview'),
    url(r'^posttopic/', post_topic, name='post_topic'),
    url(r'^listtopic/', list_topic, name='list_topic'),
)
