from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ywbserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^knowledge/', include('knowledge.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^consumption/', include('consumption.urls')),
    url(r'^mobile/', include('mobile.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^weixin/', include('weixin.urls')),
    url(r'^quan/', include('quan.urls')),
)
