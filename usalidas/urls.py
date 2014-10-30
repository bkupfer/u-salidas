# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Pages:
    # General views
    url(r'^login', 'salidas.views.login', name='login'),
    url(r'^logout', 'salidas.views.logout', name='logout'),
    url(r'^access_denied', 'salidas.views.access_denied', name='access_denied'),
    url(r'^nothing_to_do_here', 'salidas.views.nothing_to_do_here', name='nothing_to_do_here'),
    url(r'^externo.php','salidas.views.externo',name='externo'),

    # Teacher view pages
    url(r'^$', 'salidas.views.login', name='login'),
    url(r'^new_application', 'salidas.views.new_application', name='new_application'),
    url(r'^teacher_calendar', 'salidas.views.teacher_calendar', name='teacher_calendar'),
    url(r'^teachers_applications', 'salidas.views.teachers_applications', name='teachers_applications'),
    url(r'^replacement_requests', 'salidas.views.replacement_requests', name='replacement_requests'),
    url(r'^replacement_list', 'salidas.views.replacement_list', name='replacement_list'),
    url(r'^application_detail', 'salidas.views.application_detail', name='application_detail'),

    # Administrative view pages
    url(r'^list_of_applications', 'salidas.views.list_of_applications', name='list_of_applications'),
    url(r'^application_review', 'salidas.views.application_review', name='application_review'),
    url(r'^historic_calendar', 'salidas.views.historic_calendar', name='historic_calendar'),
    url(r'^list_alejandro', 'salidas.views.list_alejandro', name='list_alejandro'),
    url(r'^detail_alejandro', 'salidas.views.detail_alejandro', name='alejandro'),
    url(r'^finance_validation', 'salidas.views.finance_validation', name='finance_validation'),
    url(r'^days_validation', 'salidas.views.days_validation', name='days_validation'),

    #documents
    url(r'^getfiles', 'salidas.documentViews.getfiles',name='exportar_doc'),

    # Debuging pages

    # Django's admin site
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)