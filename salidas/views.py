from django.shortcuts import render, render_to_response, RequestContext

from salidas.models import *    #  for data
from salidas.forms import *     #  for calendar
from salidas.calendar import *  #  for calendar
from django.utils.safestring import mark_safe   #  for calendar

# Views for all users
def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))


#Views for teachers
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

def prueba(request):
    application = NewApplicationForm(request.POST or None)
    # if application.is_valid():
    #     rut1 = application.cleaned_data['rut']
    #     ct = application.cleaned_data['commission_type']
    #     fb = application.cleaned_data['financed_by']
    #     motive = application.cleaned_data['motive']
    #     newApp = Application()
    return render_to_response("prueba.html", locals(), context_instance=RequestContext(request))

def teacher_calendar(request):
    return render_to_response("teacher_calendar.html", locals(), context_instance=RequestContext(request))


# Views for administrative people
def list_of_applications(request):
    apps = Application.objects.all()
    return render_to_response("list_of_applications.html", locals(), context_instance=RequestContext(request))


def application_detail(request):
    rut_profesor = "17704795-3"  # IMPORTANTE!! este valor tiene que ser el rut del profesor
    query = Application.objects.get(rut__exact = rut_profesor)  # Application query
    comm_type = query.id_commission_type
    dest = query.id_destination
    return render_to_response("application_detail.html", locals(), context_instance=RequestContext(request))

def historic_calendar(request):
    return render_to_response("historic_calendar.html", locals(), content_type=RequestContext(request))

# Aditional views
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
