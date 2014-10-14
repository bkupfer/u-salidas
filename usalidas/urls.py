from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Pages:
    # Teacher view pages
    url(r'^$', 'salidas.views.home', name='home'),
    url(r'^new_application', 'salidas.views.new_application', name='new_application'),
    url(r'^prueba', 'salidas.views.prueba', name='prueba'),
    url(r'^teacher_calendar', 'salidas.views.teacher_calendar', name='teacher_calendar'),

    # Administrative view pages
    url(r'^list_of_applications', 'salidas.views.list_of_applications', name='list_of_applications'),
    url(r'^application_detail', 'salidas.views.application_detail', name='application_detail'),
    url(r'^historic_calendar', 'salidas.views.historic_calendar', name='historic_calendar'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    # Django's admin site
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)