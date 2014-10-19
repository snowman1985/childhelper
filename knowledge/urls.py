'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from knowledge import views

urlpatterns = patterns('',
    url(r'^add/$', views.KnowledgeFormView.as_view(success_url='/knowledge/add/')),
    url(r'^collect/',views.collectknowl, name='collectknowl'),
    url(r'^listcollect/',views.list_collection, name='list_collection'),
    url(r'^webview/$', views.web_view),
    url(r'^list/', views.list_knowledge, name='knowledge list view'),
    url(r'^cancel/',views.cancelknowl, name='cancelknowl'),
)
