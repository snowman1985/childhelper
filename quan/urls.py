'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^posttopic/', post_topic, name='post_topic'),
    url(r'^getcircletopic/', get_circletopic, name='get_circle_topic'),
#     url(r'^gettopic/', views.update, name='update'),
#     url(r'^commenttopic/', views.informationcheck, name='informationcheck'),
)
