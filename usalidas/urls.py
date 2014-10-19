from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Pages:
    # General views
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    # Teacher view pages
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^new_application', 'salidas.views.new_application', name='new_application'),
    url(r'^teacher_calendar', 'salidas.views.teacher_calendar', name='teacher_calendar'),
    url(r'^teachers_applications', 'salidas.views.teachers_applications', name='teachers_applications'),

    # Administrative view pages
    url(r'^list_of_applications', 'salidas.views.list_of_applications', name='list_of_applications'),
    url(r'^application_detail', 'salidas.views.application_detail', name='application_detail'),
    url(r'^historic_calendar', 'salidas.views.historic_calendar', name='historic_calendar'),
    url(r'^list_alejandro', 'salidas.views.list_alejandro', name='list_alejandro'),
    url(r'^detail_alejandro', 'salidas.views.detail_alejandro', name='alejandro'),

    #URL pagina prueba
   # url(r'^prueba', 'salidas.views.prueba', name='prueba'),


    # Django's admin site
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)