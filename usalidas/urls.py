from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'salidas.views.home', name='home'),
    url(r'^new_application', 'salidas.views.new_application', name='new_application'),

    # Django's admin site
    url(r'^admin/', include(admin.site.urls)),
)
