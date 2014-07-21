'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^$', MerchantMainPageView.as_view(), name='merchant_mainpage'),
    url(r'^register/', RegisterView.as_view(success_url='/merchant/'), name='register'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name':'merchant/password_change.html'},name='password_change'),
    #url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_change/done/$', MerchantHomeView.as_view(), name='password_change_done'),
    url(r'^home/', MerchantHomeView.as_view(), name='merchant_home'),
    #url(r'^commercials/promotioneffect/(\d+)/', PromotionView.as_view(), name='promotion_effect'),
    url(r'^commercials/post/', CommercialPostView.as_view(success_url='/merchant/commercials/list/'), name='commercials_post'),
    url(r'^commercials/list/', CommercialListView.as_view(), name='commercials_list'),
    url(r'^commercials/promotioneffect/(?P<commercial_id>\d+)/', PromotionView.as_view(), name='promotion_effect'),
    url(r'^commercials/', CommercialListView.as_view(), name='commercials'),
    url(r'^about$', about, name='about'),
    url(r'^findhelp/', FindHelpView.as_view(), name='findhelp'),
)

