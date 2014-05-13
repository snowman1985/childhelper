'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^posttopic/', post_topic, name='post_topic'),
    url(r'^getcircletopic/', get_circletopic, name='get_circle_topic'),
    url(r'^gettopicwebview/([0-9]*)/$', get_topic_webview, name='get_topic_webview'),
#     url(r'^gettopic/', views.update, name='update'),
    url(r'^addtopiccomment/(\d+)/$', addtopiccomment, name='addtopiccomment'),
    url(r'^addcommentwebview/(\d+)/$', addcommentwebview, name='addcommentwebview'),
)
