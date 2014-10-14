from django.shortcuts import render, render_to_response, RequestContext

from salidas.models import *    #  for data
from salidas.forms import *     #  for calendar
from salidas.calendar import *  #  for calendar
from django.utils.safestring import mark_safe   #  for calendar
from django.contrib import auth
from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.contrib.auth import  authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required

# Views for all users
def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username,password=password)
    if user is not None and user.is_active:
        # Clave correcta, y el usuario está marcado "activo"
        login(request, user)
        # Redirigir a una página de éxito.

        return redirect(new_application)
    else:
        # Mostrar una página de error
        return redirect(login)


#Views for teachers
def new_application(request):
    application = NewApplicationForm(request.POST or None)
    destinations = DestinationFormSet(request.POST or None)
    executiveReplacement = ReplacementApplicationForm(request.POST or None)
    academicReplacement = ReplacementApplicationForm(request.POST or None)
    if application.is_valid():
        if destinations.is_valid():
            if executiveReplacement.is_valid():
                if academicReplacement.is_valid():
                    #se arma la instancia Application
                    rut = Teacher.objects.get(rut="3238765-6") #EL PROFE ES EL PRIMERO EN MI LISTA
                    ct = application.cleaned_data['id_commission_type']
                    fb = application.cleaned_data['financed_by']
                    motive = application.cleaned_data['motive']
                    daysv = State.objects.get(pk=3)
                    fundsv = State.objects.get(pk=3)
                    newApp = Application(rut=rut,id_commission_type=ct,financed_by=fb,motive=motive,id_days_validation_state=daysv,id_funds_validation_state=fundsv)
                    newApp.save()
                    #se arma la instancia Destination
                    for destination in destinations:
                        country = destination.cleaned_data['country']
                        city = destination.cleaned_data['city']
                        start_date = destination.cleaned_data['start_date']
                        end_date = destination.cleaned_data['end_date']
                        newDestination = Destination(application=newApp,country=country,city=city,start_date=start_date,end_date=end_date)
                        newDestination.save()
                        #se guardan los profes reemplazantes
                        executiveReplace = executiveReplacement.cleaned_data['teacher']
                        academicReplace = academicReplacement.cleaned_data['teacher']
                        newExecutiveReplacement = Replacement(rut_teacher=executiveReplace,id_Application=newApp,id_state=daysv)
                        newAcademicReplacement = Replacement(rut_teacher=academicReplace,id_Application=newApp,id_state=daysv)
                        newExecutiveReplacement.save()
                        newAcademicReplacement.save()

    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))


def prueba(request):
    application = NewApplicationForm(request.POST or None)
    destinations = DestinationFormSet(request.POST or None)
    executiveReplacement = ReplacementApplicationForm(request.POST or None)
    academicReplacement = ReplacementApplicationForm(request.POST or None)
    if application.is_valid():
        if destinations.is_valid():
            if executiveReplacement.is_valid():
                if academicReplacement.is_valid():
                    #se arma la instancia Application
                    rut = Teacher.objects.get(rut="3238765-6") #EL PROFE ES EL PRIMERO EN MI LISTA
                    ct = application.cleaned_data['id_commission_type']
                    fb = application.cleaned_data['financed_by']
                    motive = application.cleaned_data['motive']
                    daysv = State.objects.get(pk=3)
                    fundsv = State.objects.get(pk=3)
                    newApp = Application(rut=rut,id_commission_type=ct,financed_by=fb,motive=motive,id_days_validation_state=daysv,id_funds_validation_state=fundsv)
                    newApp.save()
                    #se arma la instancia Destination
                    for destination in destinations:
                        country = destination.cleaned_data['country']
                        city = destination.cleaned_data['city']
                        start_date = destination.cleaned_data['start_date']
                        end_date = destination.cleaned_data['end_date']
                        newDestination = Destination(application=newApp,country=country,city=city,start_date=start_date,end_date=end_date)
                        newDestination.save()
                        #se guardan los profes reemplazantes
                        executiveReplace = executiveReplacement.cleaned_data['teacher']
                        academicReplace = academicReplacement.cleaned_data['teacher']
                        newExecutiveReplacement = Replacement(rut_teacher=executiveReplace,id_Application=newApp,id_state=daysv)
                        newAcademicReplacement = Replacement(rut_teacher=academicReplace,id_Application=newApp,id_state=daysv)
                        newExecutiveReplacement.save()
                        newAcademicReplacement.save()

    return render_to_response("prueba.html", locals(), context_instance=RequestContext(request))


def teacher_calendar(request):
    return render_to_response("teacher_calendar.html", locals(), context_instance=RequestContext(request))


# Views for administrative people
def list_of_applications(request):
    apps = Application.objects.all()
    return render_to_response("list_of_applications.html", locals(), context_instance=RequestContext(request))


def application_detail(request):
    id_app = 1  #  IMPORTANTE! : este valor debe ser el id de la solicitud seleccionada!
    query = Application.objects.get(pk = id_app)  # Application query
    profesor = query.rut

    comm_type = query.id_commission_type
    dest = Destination.objects.filter(application = query.id)
    return render_to_response("application_detail.html", locals(), context_instance=RequestContext(request))


def historic_calendar(request):
    return render_to_response("historic_calendar.html", locals(), content_type=RequestContext(request))


def list_alejandro(request):
    apps = Application.objects.all()
    return render_to_response("list_alejandro.html", locals(), context_instance=RequestContext(request))


def detail_alejandro(request):
    id_app = 1  #  IMPORTANTE! : este valor debe ser el id de la solicitud seleccionada!
    application = Application.objects.get(pk = id_app)
    destinations = Destination.objects.filter(application = id_app)
    teacher = application.rut
    return render_to_response("detail_alejandro.html", locals(), content_type=RequestContext(request))

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

