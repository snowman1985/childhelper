'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^posttopicwebview/(\d+)/$', post_topic_webview, name='post_topic_webview'),
    url(r'^gettopicwebview/([0-9]*)/$', get_topic_webview, name='get_topic_webview'),
    url(r'^addcommentwebview/(\d+)/(\d+)/$', addcommentwebview, name='addcommentwebview'),
    
    url(r'^posttopic/', post_topic, name='post_topic'),
    url(r'^getcircletopic/', get_circletopic, name='get_circle_topic'),
    url(r'^addcomment/$', add_comment, name='addcomment'),
)
