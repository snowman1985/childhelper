'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^refresh_tlquan_news', refresh_tlquan_news, name='refresh_tlquan_news'),
)