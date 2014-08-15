

from django.conf.urls import patterns, url

from personality import views

urlpatterns = patterns('',
  url(r'^list_person_topics/', views.list_person_topics, name='list person topics'),
  url(r'^list_person_userdemand/', views.list_person_userdemand, name='list person userdemand'),
)
