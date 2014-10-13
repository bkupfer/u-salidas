from django.shortcuts import render, render_to_response, RequestContext
from django.utils.safestring import mark_safe

from salidas.forms import *     #  for calendar
from salidas.calendar import *  #  for calendar



def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))


def new_application(request):
    application = NewApplicationForm(request.POST or None)
    destinationFormSet = DestinationFormSet(request.POST or None)
    academicReplacement = ReplacementApplicationForm(request.POST or None)
    executiveReplacement = ReplacementApplicationForm(request.POST or None)
    if application.is_valid():
        new_app = application.save(commit=False)
        new_app.save()
    if destinationFormSet.is_valid():
        new_destination = destinationFormSet.save(commit=False)
        new_destination.save()
    if academicReplacement.is_valid():
        replacement = academicReplacement.save(commit=False)
        replacement.save()
    if executiveReplacement.is_valid():
        replacement = executiveReplacement.save(commit=False)
        replacement.save()
    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))


def application_detail(request):
    CommissionType.objects
    b = CommissionType(pk=1)
    return render_to_response("application_detail.html", locals(), context_instance=RequestContext(request))


def teacher_calendar(request):
    return render_to_response("teacher_calendar.html", locals(), context_instance=RequestContext(request))


def calendar(request, year, month):
    # primero debemos obtenemos los datos de la base de datos, luego le damos la query a WorkoutCalendar
    # un ejemplo de cómo hacer esto es el que se muestra a continuación.

    # para ver el resultado o mas detalles de como se supone funciona esto, revisar el siguiente link
    #   http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/

    '''
    my_workouts = Workouts.objects.order_by('my_date').filter(
        my_date__year=year, my_date__month=month
    )

    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return render_to_response('my_template.html', {'calendar': mark_safe(cal),})  # para nuestro caso, no sé bien qué deberíamos retornar.
    '''
