# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.contrib.auth import  authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

from django.contrib.auth.models import User, Group

from salidas.forms import *
from salidas.models import *

from usalidas.email_contat_list import *

# For externo
from OpenSSL.crypto import * # verify, load_certificate, load_privatekey, Error,FILETYPE_PEM
import base64
import urllib.request

from io import StringIO
from docx import * # to generate Docs
import os, os.path
from django.views.decorators.csrf import csrf_protect

# Views for all users
# Login
def home(request):
    return render_to_response("General/login.html", locals(), context_instance=RequestContext(request))


def is_in_group(user, group):
    users_in_group = Group.objects.get(name=group).user_set.all()
    if user in users_in_group or user.is_superuser:
        return True
    else:
        return False

#externo es llamado por upasaporte, se le debe retornar un request con la sesion del usuario
#recibe el post de upasaporte, valida la firma, y si pasa hay que enviar
def externo(request):
    if request.method == "POST":
        try:
            #recibir firma todo: notece que no se puede hacer borrar del request porque es un QueryDict, es un problema?
            firma = load_privatekey(FILETYPE_PEM,base64.urlsafe_base64_decode(request.POST['firma']))
            #recibir llave publica
            certificado = load_certificate(FILETYPE_PEM, urllib.request.urlopen('https://www.u-cursos.cl/upasaporte/certificado').read(1000))
            #verificar
            verify(certificado,firma,request.POST.urlencode(), 'sha1')
            #TODO: cuando esto funcione,aqui se debe verificar que el usuario esta en nuestro sistema, y si esta loguearlo (views.login)
            '''
                dificultad del TODO: nuestro views.login autentifica al usuario usando auth.authenticate,
                si upasaporte autentifica no tendremos usuario ni clave, no sabemos que informacion del profe
                o de la persona nos manda upasaporte.
                ahi aparece como autentificar sin autentificar
                 http://stackoverflow.com/questions/2787650/manually-logging-in-a-user-without-password
            '''
            #retorna un request con el usuario
            return  redirect('login')
        except Error:
            print("ERROR EXTERNO")#todo: agregar mensaje en caso de ingresar mal los datos
            return redirect('access_denied') # todo:arreglar access_denied para usuarios externos e internos

@csrf_protect
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                session_id = request.user.id
                if is_in_group(user, 'professor'):
                    return redirect('teachers_applications')
                elif is_in_group(user, 'angelica'):
                    return redirect('days_validation')
                elif is_in_group(user, 'magna'):
                    return redirect('list_of_applications')
                elif is_in_group(user, 'alejandro'):
                    return redirect('list_alejandro')
                else:
                    return redirect('nothing_to_do_here')
            else:
                print("user no existe")
                return render_to_response("General/login.html", locals(), context_instance=RequestContext(request))
        else:
            print("error filling up the login form")
    else:
        form = AuthenticationForm()
    return render_to_response("General/login.html", locals(), context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return redirect(login)


# Not registered user (student of something..)
def nothing_to_do_here(request):
    return render_to_response("General/nothing_to_do_here.html", locals(), context_instance=RequestContext(request))


# Access denied
def access_denied(request):
    return render_to_response("General/access_denied.html", locals(), context_instance=RequestContext(request))


#Views for teachers
#Este es el formulario prototipo de financia
def financeForm(finance, newApp, id_finance_type):
    if finance.is_valid():
        try:
            checkbox = finance.cleaned_data['checkbox']
            if checkbox:
                currency = finance.cleaned_data['id_currency']
                amount = finance.cleaned_data['amount']
                type = FinanceType.objects.get(pk=id_finance_type)
                newFinance = Finance(id_application=newApp,id_finance_type=type, id_currency=currency, amount=amount)
                newFinance.save()
        except:
            print("error en financeForm method. view.py")


def destinationForm(destination, newApp):
    if destination.is_valid():
        try:
            country = destination.cleaned_data['country']
            city    = destination.cleaned_data['city']
            start_date = destination.cleaned_data['start_date']
            end_date= destination.cleaned_data['end_date']
            destiny = Destination(application=newApp,country=country, city=city, start_date=start_date, end_date=end_date)
            destiny.save()
        except:
            print("error en destinationForm method. view.py")


def documentForm(doc, newApp):
    if doc.is_valid():
        try:
            file = doc.cleaned_data['file']
            newDocument = Document(id_application = newApp, file = file)
            newDocument.save()
        except:
            file = None


@login_required
def new_application(request):
    user=request.user
    application = NewApplicationForm(request.POST or None,prefix="application")
    destinations = DestinationFormSet(request.POST or None,prefix="destinations")
    financeFormSet = FinanceFormSet(request.POST or None,prefix="finance")
    documents = DocumentFormSet(request.POST or None, request.FILES or None, prefix="documents")

    if len(request.POST) != 0:
        if application.is_valid() and destinations.is_valid() and request.POST['repteachers'] and request.POST['acteachers']:
            # Applications instance
            id_teacher = Teacher.objects.get(user=request.user)
            ct = application.cleaned_data['id_commission_type']
            motive = application.cleaned_data['motive']
            fb = application.cleaned_data['financed_by']
            daysv = State.objects.get(pk=1)     # pendiente
            fundsv = State.objects.get(pk=1)    # pendiente

            newApp = Application(id_Teacher = id_teacher, id_commission_type = ct, motive = motive, financed_by = fb,
                                 id_days_validation_state = daysv, id_funds_validation_state = fundsv)
            newApp.save()

            #agregarle estado a la App
            #estado pendiente dcc
            state = ApplicationState.objects.get(pk=1)  # pendiente aprobacion
            stateApp = ApplicationHasApplicationState(id_application=newApp, id_application_state=state)
            stateApp.save()

            # replacement teacher information
            executiveReplace = request.POST['repteachers'] # executiveReplacement.cleaned_data['repteachers']
            academicReplace  = request.POST['acteachers']  #  academicReplacement.cleaned_data['acteachers']
            newExecutiveReplacement = Replacement(rut_teacher=Teacher.objects.get(pk=executiveReplace), id_Application=newApp, id_state=daysv, type=ReplacementType.objects.get(type="Docente"))
            newAcademicReplacement  = Replacement(rut_teacher=Teacher.objects.get(pk=academicReplace),  id_Application=newApp, id_state=daysv, type=ReplacementType.objects.get(type="Academico"))
            newExecutiveReplacement.save()
            newAcademicReplacement.save()

            # money
            i = 1
            for finance in financeFormSet:
                financeForm(finance, newApp, i)
                i += 1

            # destinations
            for destination in destinations:
                destinationForm(destination, newApp)

            # documents
            for document in documents:
                documentForm(document, newApp)

            # signature
            try:
                asignature = request.FILES['signature']
                extention = asignature.__str__().split(".")[1]
                if extention == "jpg" or extention == "jpeg" or extention == "png":
                    id_teacher.signature.delete()
                    id_teacher.signature = asignature
                    id_teacher.save()
                else:
                    messages.error(request, "Formato de firma invalido. Usar '.jpg' o '.png'.")
            except:
                asignature=None

            # sending notification mail
            subject = "Nueva solicitud de salida"
            message = "El docente " + id_teacher.__str__() + " ha enviado una nueva solicitud de salida.\n\n-- Este correo fue generado automaticamente, no lo responda."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { EMAIL_MAGNA }, fail_silently = False)

            messages.success(request, 'Solicitud enviada exitosamente!')
            return redirect(teachers_applications)
            # Applications instance
        else:
            # for error display
            err = 'Error en el envío del formulario.'
            if not application.is_valid():
                err = err + '\nInformación del viaje incompleta'
            if not destinations.is_valid():
                err = err + '\nInformación respecto de los destinos incompleta.'
            if not request.POST['repteachers'] or not request.POST['acteachers']:
                err = err + '\nDebe escojer sus profesores reemplazantes.'

            messages.error(request, err)

    executiveReplacement = ReplacementApplicationForm(request.POST, user, prefix="executive")
    academicReplacement  = AcademicReplacementApplicationForm(request.POST, user,prefix="academic")

    return render_to_response("Professor/new_application_form.html", locals(), context_instance=RequestContext(request))

@login_required
def teacher_calendar(request):
    teacher = Teacher.objects.filter(user=request.user.id)  # me huele que es mejor usar 'get(rut=rut)', lo dejaré como 'filter' por ahora, para que no falle con bd vacía. idem para teachers_applications
    return render_to_response("Professor/teacher_calendar.html", locals(), context_instance=RequestContext(request))


@login_required
def teachers_applications(request):
    teacher = Teacher.objects.get(user=request.user.id)
    apps = Application.objects.filter(id_Teacher=teacher).order_by('creation_date').reverse()
    return render_to_response("Professor/teachers_applications.html", locals(), context_instance=RequestContext(request))


@login_required
def replacement_list(request):
    teacher= Teacher.objects.filter(user=request.user.id)
    replacements = Replacement.objects.filter(rut_teacher=teacher)
    return render_to_response("Professor/replacement_list.html", locals(), context_instance=RequestContext(request))


#todo: bloquear obtencion de id que no pertenece a usuario CON UN TEST?
@login_required
def replacement_requests(request):
    replacement = Replacement.objects.get( pk = request.GET['id'] )

    if 'accept_button' in request.POST:
        replacement.id_state = State.objects.get(pk=2)
        replacement.save()
        return redirect('replacement_list')

    if 'reject_button' in request.POST:
        replacement.id_state = State.objects.get(pk=3)
        replacement.save()
        return redirect('replacement_list')

    return render_to_response("Professor/replacement_requests.html", locals(), context_instance=RequestContext(request))


@login_required
def application_detail(request):
    id_app = request.GET['id']
    try:
        app = Application.objects.get(pk = id_app)
        profesor = app.id_Teacher
        profesor_user = app.id_Teacher.user
        user_id = request.user.id
    except: # application dosent excist -- stil do not reveal that it dosent exist.
        return redirect(access_denied)

    if (profesor_user.id != user_id):
        return redirect(access_denied)

    comm_type = app.id_commission_type
    dest = Destination.objects.filter(application = app.id)
    replacements = app.get_replacements

    return render_to_response("Professor/application_detail.html", locals(), context_instance=RequestContext(request))


@login_required
def my_information(request):
    has_previous_signature = False
    if Teacher.objects.get(pk = request.user.id).signature != "":
        has_previous_signature = True

    prof = Teacher.objects.get(pk = request.user.id)
    print(prof)

    teacher_signature = TeacherSignatureForm(request.FILES or None)

    return render_to_response("Professor/my_information.html", locals(), context_instance=RequestContext(request))


# Views for administrative people
# Magna
@login_required
def list_of_applications(request):
    apps = Application.objects.all()
    return render_to_response("Magna/list_of_applications.html", locals(), context_instance=RequestContext(request))


@login_required
def application_review(request):
    id_app = request.GET['id']
    app = Application.objects.get(pk = id_app)
    profesor = app.id_Teacher
    comm_type = app.id_commission_type
    dest = Destination.objects.filter(application = app.id)
    replacements = app.get_replacements
    finances = app.get_finances()
    if len(request.POST) != 0:
        if 'accept_button' in request.POST:
            id_state = 2    # pendiente dcc
        if 'reject_button' in request.POST:
            id_state = 4    # rechazado

        state = ApplicationState.objects.get(pk = id_state)
        stateApp = ApplicationHasApplicationState(id_application = app, id_application_state=state)
        stateApp.save()
        return redirect("list_of_applications")

    return render_to_response("Magna/application_review.html", locals(), context_instance=RequestContext(request))


@login_required
def historic_calendar(request):
    return render_to_response("Magna/historic_calendar.html", locals(), content_type=RequestContext(request))


# Views Alejandro
@login_required
def list_alejandro(request):
    apps = Application.objects.all()
    return render_to_response("Alejandro/list_alejandro.html", locals(), context_instance=RequestContext(request))

@csrf_protect
@login_required
def detail_alejandro(request):
    id_app = request.GET['id']
    application = Application.objects.get(pk = id_app)
    destinations = Destination.objects.filter(application = id_app)
    teacher = application.id_Teacher
    finances=Finance.objects.filter(id_application=id_app)
    return render_to_response("Alejandro/detail_alejandro.html", locals(), content_type=RequestContext(request))


def finance_validation(request):
    return render_to_response("Alejandro/finance_validation.html", locals(), content_type=RequestContext(request))


# Angelica
def days_validation(request):
    return render_to_response("Angelica/days_validation.html", locals(), content_type=RequestContext(request))



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

