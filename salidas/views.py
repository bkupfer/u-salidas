# -*- coding: utf-8 -*-
from django.core.files.images import get_image_dimensions
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404,HttpResponsePermanentRedirect
from django.contrib import auth
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import  authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from salidas.forms import *
from salidas.models import *
from salidas.models import Document as DocumentModel

from usalidas.email_contact_list import *
from django.views.generic.edit import UpdateView

# For externo
from OpenSSL.crypto import * # verify, load_certificate, load_privatekey, Error,FILETYPE_PEM
import base64
import urllib.request

from io import StringIO
from docx import * # to generate Docs
import os, os.path
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from salidas.calendar import *
import traceback
import json

# Views for all users
def home(request):
    return render_to_response("General/login.html", locals(), context_instance=RequestContext(request))


def is_in_group(user, group):
    users_in_group = Group.objects.get(name=group).user_set.all()
    if user in users_in_group or user.is_superuser:
        return True
    else:
        return False


# externo es llamado por upasaporte, se le debe retornar un request con la sesion del usuario
# recibe el post de upasaporte, valida la firma, y si pasa hay que enviar
@csrf_exempt
def externo(request):
    if request.method == "POST":
        try:
            #recibir firma todo: notese que no se puede hacer borrar del request porque es un QueryDict, es un problema?
            #firma = load_privatekey(FILETYPE_PEM,base64.urlsafe_b64decode(request.POST['firma']))
            #recibir llave publica
            #certificado = load_certificate(FILETYPE_PEM, urllib.request.urlopen('https://www.u-cursos.cl/upasaporte/certificado').read())
            #verificar
            #verify(certificado,firma,"holahola", 'sha1')
            #retorna un request con el usuario
            username=request.POST['rut']
            user = auth.authenticate(username=username, password="ing")
            auth.login(request,user)
            s=SessionStore()
            s['user_id']=request.user.username
            s.save()
            if user is not None and user.is_active:
                session_key = s.session_key
                auth.logout(request)
                return HttpResponse('http://usalidas.dcc.uchile.cl/success/?s=%s' % session_key)
            return  HttpResponse("Ingrese con una cuenta válida")
        except Error:
            print("ERROR EXTERNO")#todo: agregar mensaje en caso de ingresar mal los datos
            return redirect('access_denied') # todo:arreglar access_denied para usuarios externos e internos
    return redirect('access_denied')


@csrf_exempt
def success(request):
    session = request.GET['s']
    s= Session.objects.get(session_key=session)
    user = auth.authenticate(username=s.get_decoded().get('user_id'), password="ing")
    auth.login(request,user)
    if is_in_group(user, 'professor'):
        teacher = Teacher.objects.get(user = user.id)
        if teacher.mail == None or teacher.mail == "" or teacher.signature == None or teacher.signature == "":
            return redirect('my_information')
        else:
            return redirect('teachers_applications')
    elif is_in_group(user, 'angelica'):
        request.session['tabactive']= 'liPA'
        return redirect('list_angelica')
    elif is_in_group(user, 'magna'):
        request.session['tabactive']= 'liPA'
        return redirect('list_of_applications')
    elif is_in_group(user, 'alejandro'):
        return redirect('list_alejandro')
    else:
        auth.logout(request)
        return redirect('nothing_to_do_here')


@csrf_exempt
def login2(request):
    return render_to_response("General/login2.html", locals(), context_instance=RequestContext(request))


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
                    prof = Teacher.objects.get(user = user.id)
                    if prof.mail == None or prof.mail == "" or prof.signature == None or prof.signature == "":
                        return redirect('my_information')
                    else:
                        return redirect('teachers_applications')
                elif is_in_group(user, 'angelica'):
                    return redirect('list_angelica')
                elif is_in_group(user, 'magna'):
                    request.session['tabactive']= 'liPA'
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
#Este es el formulario prototipo de financia :)
def financeForm(finance, newApp, id_finance_type):

    if finance.is_valid():
        type = FinanceType.objects.get(pk=id_finance_type)
        currency_exist = False
        amount_exist = False
        fb_exist = False
        try:
            currency = finance.cleaned_data['id_currency']
            currency_exist = True
        except Exception:
            pass
        try:
            amount = finance.cleaned_data['amount']
            amount_exist = True
        except Exception:
            pass
        try:
            fb = finance.cleaned_data['financed_by']
            fb_exist = True
        except Exception:
            pass
        if currency_exist and amount_exist and fb_exist:
            newFinance = Finance(id_application=newApp,id_finance_type=type,financed_by=fb, id_currency=currency, amount=amount)
            newFinance.save()
        else:
            print('no guarde: ' + str(type))
            #codigo para guardar finances vacios
            #newFinance = Finance(id_application=newApp,id_finance_type=type)
            #newFinance.save()
    else:
        print("finance not valid")


def destinationForm(destination, newApp):
    if destination.is_valid():
        try:
            country = destination.cleaned_data['country']
            city    = destination.cleaned_data['city']
            other_city = destination.cleaned_data['other_city']
            start_date = destination.cleaned_data['start_date']
            end_date= destination.cleaned_data['end_date']
            motive = destination.cleaned_data['motive']

            if other_city != "":
                city = other_city
            destiny = Destination(application=newApp,country=country, city=city, start_date=start_date, end_date=end_date,motive=motive)

            destiny.save()
        except:
            print("error en destinationForm method. view.py")
    else:
        print("error en destinationForm method. view.py 2")
        print(destination.errors)

def documentForm(doc, newApp):
    if doc.is_valid():
        try:
            file = doc.cleaned_data['file']
            newDocument = DocumentModel(id_application = newApp, file = file)
            newDocument.save()
        except:
            file = None

@login_required
def new_application(request):
    user = request.user
    id_teacher = Teacher.objects.get(user = request.user)
    if id_teacher.mail == "" or id_teacher.signature == "":
        messages.error(request, 'Debe ingresar sus datos antes de enviar una solicitud.')
        return redirect(my_information)

    application = NewApplicationForm(request.POST or None,prefix="application")
    destinations = DestinationFormSet(request.POST or None,prefix="destinations")
    financeFormSet = FinanceFormSet(request.POST or None,prefix="finance")
    documents = DocumentFormSet(request.POST or None, request.FILES or None, prefix="documents")

    if request.method == 'POST':
        valid_dest= False
        valid_finance= True
        if destinations.is_valid():
            for dest in destinations:
                start_date = dest.cleaned_data.get('start_date')
                end_date = dest.cleaned_data.get('end_date')
                if start_date != None or end_date != None:
                    if start_date<=end_date and start_date.year == end_date.year:
                        valid_dest=True
                else:
                    break
        # for finance in financeFormSet:
        #     if finance.is_valid():
        #         valid_finance = True
        #     else:
        #         dict = finance.errors.as_data()
        #         #si contiene 0->valido,1->invalido,2->el formset sigue siendo valido
        #         if len(dict) == 1:
        #             valid_finance = False
        #             break
        if application.is_valid() and valid_dest and valid_finance and request.POST['repteachers'] and request.POST['acteachers']:
            # Applications instance
            id_teacher = Teacher.objects.get(user=request.user)
            ct = application.cleaned_data['id_commission_type']
            daysv = State.objects.get(pk=1)     # pendiente
            fundsv = State.objects.get(pk=1)    # pendiente
            systemInformation = SystemInformation.objects.get(pk=1)
            director=systemInformation.director
            newApp = Application(id_Teacher = id_teacher, id_commission_type = ct,id_days_validation_state = daysv,
                                 id_funds_validation_state = fundsv, directors_name = director)
            newApp.save()
            # Application state: Pendiente Aprobacion
            state = ApplicationState.objects.get(pk=1)
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

            used_days = newApp.compute_used_days()
            newApp.used_days = used_days
            newApp.save()

            # documents
            for document in documents:
                documentForm(document, newApp)

            # sending notification mail
            subject = "Nueva solicitud de salida"
            message = "El docente " + id_teacher.__str__() + " ha enviado una nueva solicitud de salida.\n\n-- Este correo fue generado automaticamente, no lo responda."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { EMAIL_MAGNA }, fail_silently = False)

            messages.success(request, 'Solicitud enviada exitosamente!')
            return redirect(teachers_applications)

        else:
            #DEPRECATED
            err = 'Error en el envío del formulario.'
            if not application.is_valid():
                err = err + '\nInformación del viaje incompleta.'
            if not valid_finance:
                err = err + '\nInformación de montos solicitados incompleta, cada monto debe estar asociado a un tipo de moneda.'
            if not destinations.is_valid():
                err = err + '\nInformación respecto de los destinos incompleta.'
            if not request.POST['repteachers'] or not request.POST['acteachers']:
                err = err + '\nDebe seleccionar sus profesores reemplazantes.'
            if not valid_dest:
                err += '\nLas fechas de fin del viaje deben ser mayores o iguales a las de inicio del viaje.'
            #YA NO MOSTRAREMOS ESTOS ERRORES
            #messages.error(request, err)

    executiveReplacement = ReplacementApplicationForm(request.POST, user, prefix="executive")
    academicReplacement  = AcademicReplacementApplicationForm(request.POST, user,prefix="academic")

    return render_to_response("Professor/new_application_form.html", locals(), context_instance=RequestContext(request))


@login_required
def teacher_calendar(request):
    teacher = Teacher.objects.get(user = request.user)
    year, month = date.today().year, date.today().month
    if request.method == 'POST':
        year = int(request.POST['year'])
        month = int(request.POST['month'])
        if 'prev' in request.POST:
            month = (month - 1)
            if month == 0:
                month = 12
                year -= 1
        if 'next' in request.POST:
            month = (month + 1) % 13
            if month == 0:
                month += 1
                year += 1

    used_weeks = int(teacher.get_used_days() / 7)

    calendar = my_calendar(request, year, month)
    return render_to_response("Professor/teacher_calendar.html", {'teacher': teacher, 'used_weeks': used_weeks,'calendar': mark_safe(calendar), 'year': year, 'month':month}, context_instance=RequestContext(request))


# teachers calendar creation
def my_calendar(request, year, month):
    teacher = Teacher.objects.get(user = request.user)
    my_apps = Application.objects.filter(id_Teacher = teacher).order_by('creation_date')
    valid_dests = []
    for my_app in my_apps:
        for dest in my_app.get_destinations():
            if dest.start_date.year == year and dest.start_date.month == month:
                valid_dests.append(dest)
    return ApplicationCalendar(valid_dests).formatmonth(year, month)


#@csrf_protect
@login_required
def teachers_applications(request):
    teacher = Teacher.objects.get(user = request.user)
    apps = Application.objects.filter(id_Teacher=teacher).order_by('creation_date').reverse()
    return render_to_response("Professor/teachers_applications.html", locals(), context_instance=RequestContext(request))


@login_required
def replacement_list(request):
    teacher= Teacher.objects.filter(user=request.user.id)
    replacements = Replacement.objects.filter(rut_teacher=teacher)
    return render_to_response("Professor/replacement_list.html", locals(), context_instance=RequestContext(request))




def courses_with_modulesToList(courses_with_modules):
    list = []
    for course in courses_with_modules:
        for module in courses_with_modules[course]:
            #entry = {'start':module.get_start_time(), 'end':module.get_end_time(), 'title': course.name}
            list+=(course.name,module.get_week_day_number(),module.get_start_time(),module.get_end_time())
    return list


#todo: bloquear obtencion de id que no pertenece a usuario
@login_required
def replacement_requests(request):
    replacement = Replacement.objects.get(pk=request.GET['id'])
    teacher = replacement.rut_teacher
    appliant_teacher = replacement.get_appliant_teacher()
    teacher_courses_list = courses_with_modulesToList(teacher.get_courses_with_modules())
    appliant_teacher_courses_list = courses_with_modulesToList(appliant_teacher.get_courses_with_modules())

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
    finances = Finance.objects.filter(id_application=id_app)
    replacements = app.get_replacements
    return render_to_response("Professor/application_detail.html", locals(), context_instance=RequestContext(request))


@login_required
def my_information(request):
    teacher = Teacher.objects.get(user = request.user)
    form = MyInformation(request.POST or None)
    signature = TeachersSignature2(request.FILES or None)

    if request.method == 'POST':

        if form.is_valid() and len(request.FILES) != 0:
            email = form.cleaned_data['email']
            jornada = form.cleaned_data['jornada']

            sign = request.FILES['sign']
            dimentions = get_image_dimensions(sign)
            correct_dimentions = False
            if (250 <= dimentions[0] and dimentions[0] <= 500) and (250 <= dimentions[1] and dimentions[1] <= 500):
                correct_dimentions = True

            sign_extention =  sign.__str__().split(".")[1]
            size_of_sign = 1 * 1024 * 1024 + 1024 # 1K for error
            if (sign_extention == "jpg" or sign_extention == "jpeg" or sign_extention == "png") and sign._size <= size_of_sign and correct_dimentions:
                teacher.mail = email
                teacher.working_day = jornada
                teacher.signature.delete()
                teacher.signature = sign
                teacher.save()
                messages.success(request, 'Datos actualizados exitosamente!')
            else:
                if not correct_dimentions:
                    err = 'La firma debe tener dimensiones entre (250x250) y (500x500).'
                else:
                    err = 'La firma debe estar en formato .jpg o .png, y pesar menos de 1MB.'
                messages.error(request, err)
        else:
            messages.error(request, 'Debe ingresar todos los campos obligatorios.')

    return render_to_response("Professor/my_information.html", locals(), context_instance=RequestContext(request))


# Views for administrative people
# Magna
@login_required
def list_of_applications(request):
    if request.GET.get('t') == None:
        try:
            tabActive = request.session['tabactive']
        except:
            tabActive = "liPA"
    else:
        tabActive = "liPA"

    apps = Application.objects.all()
    return render_to_response("Magna/list_of_applications.html",locals(),context_instance=RequestContext(request))


@login_required
def notifyTeacher(teacher, replacement):
    subject = "Nueva Solicitud de Reemplazo"
    message = "El profesor " + teacher.__str__() + " le ha enviado una nueva solicitud de reemplazo.\n\n--Este correo fue generado automaticamente."
    send_mail(subject, message, settings.EMAIL_HOST_USER, { replacement.mail }, fail_silently = True)

@login_required
def edit_application(request):
    id_app = request.GET['id']
    last_app = Application.objects.get(pk=id_app)
    app_state = last_app.get_state().state
    if app_state == "Terminada":
        raise Http404
    user=request.user
    teacher=last_app.id_Teacher
    application = NewApplicationFormEdit(request.POST or None,prefix="application",initial={'id_commission_type':last_app.id_commission_type,'used_days':last_app.used_days, 'directors_name':last_app.directors_name})
    last_finances = last_app.get_finances()
    fins=[]
    finance_types=FinanceType.objects.all()
    for finance_type in finance_types:
        try:
            finance=Finance.objects.get(id_application=last_app,id_finance_type=finance_type)
            if finance.amount != None and finance.id_currency !=None and finance.financed_by != None:
                fins.append({'amount':finance.amount,'id_currency':finance.id_currency,'financed_by':finance.financed_by})
            else:
                fins.append({'amount':'','id_currency':'','financed_by':''})
        except:
            print(traceback.format_exc())
            fins.append({'id_finance_type':finance_type})
    financeFormSet = FinanceFormSet_Edit(request.POST or None,prefix="finance",initial=fins)
    last_dests = Destination.objects.filter(application = last_app.id)
    dess=[]
    for dest in last_dests:
        dess.append({'country':dest.country,'city':dest.city,'start_date':dest.start_date,'end_date':dest.end_date,
                     'motive':dest.motive})
    destinations = DestinationFormSet_Edit(request.POST or None,prefix="destinations",initial=dess)
    last_replacements = last_app.get_replacements()
    for reps in last_replacements:
        if str(reps.type)=="Docente":
            docrep=reps.rut_teacher
        else:
            acrep=reps.rut_teacher
    #try:
    #    print(DocumentModel)
    #    last_docs=DocumentModel.objects.filter(id_application=last_app)
    #    in_docs=[]
    #    for doc in last_docs:
    #        in_docs.append({'file':doc.file})
    #except:
    #    in_docs=[]
    #documents = DocumentFormSet_Edit(request.POST or None, request.FILES or None, prefix="documents",initial=in_docs)

    if request.method == 'POST':
        valid_dest=False
        if destinations.is_valid():
            for dest in destinations:
                start_date = dest.cleaned_data.get('start_date')
                end_date = dest.cleaned_data.get('end_date')
                if start_date != None or end_date != None:
                    if start_date<=end_date and start_date.year == end_date.year:
                        valid_dest=True
                else:
                    break
        else:
            print(destinations.errors)
        #TODO: validar financeFormSet.is_valid() y hacer que no pasen cosas raras
        if application.is_valid() and valid_dest and request.POST['repteachers'] and request.POST['acteachers']:
            last_dests.delete()
            # Applications instance
            print(request.POST)
            id_teacher = teacher #Teacher.objects.get(teacher=teacher)
            ct = application.cleaned_data['id_commission_type']
            used_days = application.cleaned_data['used_days']

            last_app.id_commission_type=ct
            last_app.used_days=used_days
            last_app.save()

            # replacement teacher information
            executiveReplace = Teacher.objects.get(pk=request.POST['repteachers']) # executiveReplacement.cleaned_data['repteachers']
            ex_rep=Replacement.objects.get(id_Application=last_app,type=ReplacementType.objects.get(type="Docente"))
            if ex_rep.rut_teacher.rut != executiveReplace.rut:
                notifyTeacher(id_teacher,ex_rep.rut_teacher)
                ex_rep.id_state = State.objects.get(pk=1) #Pendiente
            ex_rep.rut_teacher=executiveReplace
            ex_rep.save()
            academicReplace = Teacher.objects.get(pk=request.POST['acteachers'])  # academicReplacement.cleaned_data['acteachers']
            ac_rep=Replacement.objects.get(id_Application=last_app,type=ReplacementType.objects.get(type="Academico"))
            if ac_rep.rut_teacher.rut != academicReplace.rut:
                notifyTeacher(id_teacher,ac_rep.rut_teacher)
                ac_rep.id_state = State.objects.get(pk=1) #Pendiente
            ac_rep.rut_teacher=academicReplace
            ac_rep.save()

            # money
            i = 1
            #delete other finances
            last_finances.delete()
            for finance in financeFormSet:
                financeForm(finance, last_app, i)
                i += 1

            # destinations
            # delete ther destinations

            for destination in destinations:
                destinationForm(destination, last_app)

            #TODO delete other documents?
            #try:
            #    last_docs.delete()
            #except:
            #    print("error deleting last documents (?)")
            #for document in documents:
            #    documentForm(document, last_app)

            # sending notification mail
            subject = "Solicitud de salida modificada"
            message = "La solicitud de salida realizada el " + str(last_app.creation_date) + " ha sido modificada.\n\n-- Este correo fue generado automaticamente."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { id_teacher.mail }, fail_silently = True)

            # messages.success(request, 'Solicitud modificada exitosamente!')
            return redirect(list_of_applications)
        else:
            # for error display
            err = 'Error en el envío del formulario.'
            if not application.is_valid():
                err = err + '\nInformación del viaje incompleta'
            if not destinations.is_valid():
                err = err + '\nInformación respecto de los destinos incompleta.'
            if not financeFormSet.is_valid():
                err = err + '\nInformación respecto de los montos solicitados incompleta.'
            if not request.POST['repteachers'] or not request.POST['acteachers']:
                err = err + '\nDebe escojer sus profesores reemplazantes.'
            if not valid_dest:
                err += '\nLas fechas de fin del viaje deben ser mayores o iguales a las de inicio del viaje'
            messages.error(request, err)

    executiveReplacement = ReplacementApplicationForm(request.POST, teacher.user, prefix="executive",initial=docrep)
    academicReplacement  = AcademicReplacementApplicationForm(request.POST, teacher.user,prefix="academic",initial=acrep)

    return render_to_response("Magna/edit_application_form.html", locals(), context_instance=RequestContext(request))


def saveState(app, id_state):
    state = ApplicationState.objects.get(pk=id_state)
    stateApp = ApplicationHasApplicationState(id_application=app, id_application_state=state)
    stateApp.save()


@login_required
def application_review(request):
    id_app = request.GET['id']
    app = Application.objects.get(pk = id_app)
    actual_state = app.get_state()
    teacher = app.id_Teacher
    comm_type = app.id_commission_type
    dest = Destination.objects.filter(application = app.id)
    replacements = app.get_replacements()
    finances = app.get_finances()
    report_receive_form = ReportReceiveForm(request.POST or None)

    if len(request.POST) != 0:
        if 'accept_button' in request.POST:
            id_state = 2    # pendiente dcc
            subject = "Nueva solicitud de salida"
            message = "Se ha enviado una nueva solicitud de salida.\n\n-- Este correo fue generado automaticamente."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { EMAIL_ANGELICA, EMAIL_ALEJANDRO }, fail_silently = True)
            messages = "El profesor " + teacher.__str__() + " le ha enviado una nueva solicitud de reemplazo.\n\n--Este correo fue generado automaticamente."
            for replacement in replacements:
                if replacement.rut_teacher.mail != "":
                    send_mail(subject, message, settings.EMAIL_HOST_USER, { replacement.rut_teacher.mail }, fail_silently = True)
            saveState(app, id_state)
            request.session['tabactive'] = 'liPDCC'
            return redirect('list_of_applications')
        if 'reject_button' in request.POST:
            id_state = 5    # rechazado
            saveState(app, id_state)
            request.session['tabactive'] = 'liTdo'
            return redirect('list_of_applications')
        if 'report_sent_button' in request.POST:
            id_state = 3    # pendiente facultad
            saveState(app, id_state)
            request.session['tabactive'] = 'liPF'
            return redirect('list_of_applications')
        if 'report_receive_button_accepted' in request.POST:
            id_state = 4    # terminado
            subject = "Nueva solicitud de salida aprobada"
            message = "Su solicitud de salida ha sido aprobada.\n\n-- Este correo fue generado automaticamente."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { teacher.mail }, fail_silently = False)
            saveState(app, id_state)
            request.session['tabactive'] = 'liTda'
            return redirect('list_of_applications')
        if 'report_receive_button_rejected' in request.POST:
            id_state = 1    # pendiente aprobacion
            if report_receive_form.is_valid():
                obs = report_receive_form.cleaned_data['obs']
                subject = "Nueva solicitud de salida rechazada por facultad"
                message = "Su solicitud de salida ha sido rechazada por la facultad, y está volviendo a ser revisada por el departamento."
                if obs != "":
                    message += "\n\nSe agregó la siguiente observación:\n" + obs
                message += "\n\n-- Este correo fue generado automaticamente."
                send_mail(subject, message, settings.EMAIL_HOST_USER, { teacher.mail }, fail_silently = True)
                saveState(app, id_state)
                request.session['tabactive'] = 'liPA'
                return redirect('list_of_applications')
            else:
                print("report_receive_form invalid")

    return render_to_response("Magna/application_review.html", locals(), context_instance=RequestContext(request))


@login_required
def historic_calendar(request):
    year, month = date.today().year, date.today().month
    if request.method == 'POST':
        year = int(request.POST['year'])
        month = int(request.POST['month'])
        if 'prev' in request.POST:
            month = (month - 1)
            if month == 0:
                month = 12
                year -= 1
        if 'next' in request.POST:
            month = (month + 1) % 13
            if month == 0:
                month += 1
                year += 1

    calendar = my_historic_calendar(request, year, month)
    return render_to_response("Magna/historic_calendar.html", {'calendar': mark_safe(calendar), 'year': year, 'month':month}, context_instance=RequestContext(request))


#  historic calendar -- calendar showing all applications
def my_historic_calendar(request, year, month):
    my_apps = Application.objects.order_by('creation_date')
    valid_dests = []
    for my_app in my_apps:
        for dest in my_app.get_destinations():
            if dest.start_date.year == year and dest.start_date.month == month:
                valid_dests.append(dest)
    return HistoricCalendar(valid_dests).formatmonth(year, month)


# Views Alejandro
@csrf_protect
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
    finances = Finance.objects.filter(id_application=id_app)
    user = request.user
    reject_observation = RejectObservationsForm(request.POST or None)

    if len(request.POST) != 0:
        #si acepta mandar mail magna
        if 'accept_button' in request.POST:
            application.id_funds_validation_state = State.objects.get(pk=2) #estado aceptado
            application.save()
            subject = "Validacion fondos Salida"
            message = "En relación a la salida N°:"+id_app+". Se han validado los fondos de la salida.\n\n-- Este correo fue generado automáticamente."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { EMAIL_MAGNA }, fail_silently = True)
            request.session['tabactive'] = 'liPDCC'
            return redirect('list_alejandro')
        #si rechaza mandar mail profe y magna
        if 'reject_button' in request.POST:
            request.session['tabactive'] = 'liPDCC'
            application.id_funds_validation_state = State.objects.get(pk=3)
            application.save()
            if reject_observation.is_valid():
                obs = reject_observation.cleaned_data['obs']
                subject = "Solicitud Salida: Validacion de fondos Rechazada"
                message = "La solicitud de salida N°"+id_app+" ha sido rechazada por la jefa administrativa."
                if obs != "":
                    message += "\n\nSe agregó la siguiente observación:\n" + obs
                message += "\n\n-- Este correo fue generado automaticámente."
                send_mail(subject, message, settings.EMAIL_HOST_USER, { teacher.mail, EMAIL_MAGNA }, fail_silently = True)
                return redirect('list_alejandro')
            else:
                print("report_receive_form invalid")
            return redirect('list_alejandro')


    return render(request, 'Alejandro/detail_alejandro.html', locals())
    #return render_to_response("Alejandro/detail_alejandro.html", locals(), content_type=RequestContext(request))


@csrf_protect
@login_required
def finance_validation(request):
    return render_to_response("Alejandro/finance_validation.html", locals(), content_type=RequestContext(request))


# Angelica
@csrf_protect
@login_required
def days_validation(request):
    user = request.user
    id_app = request.GET['id']
    app = Application.objects.get(pk = id_app)
    actual_state = app.get_state()
    teacher = app.id_Teacher
    comm_type = app.id_commission_type
    dest = Destination.objects.filter(application = app.id)
    replacements = app.get_replacements()
    report_receive_form = RejectObservationsForm(request.POST or None)

    if len(request.POST) != 0:
        #si acepta mandar mail magna
        if 'accept_button' in request.POST:
            app.id_days_validation_state = State.objects.get(pk=2)
            app.save()
            subject = "Validacion Salida"
            message = "En relación a la salida N°:"+id_app+". Se han validado los días utilizados y el horario del profesor reemplazante.\n\n-- Este correo fue generado automáticamente."
            send_mail(subject, message, settings.EMAIL_HOST_USER, { EMAIL_MAGNA }, fail_silently = True)
            request.session['tabactive'] = 'liPDCC'
            return redirect('list_angelica')
        #si rechaza mandar mail profe y magna
        if 'reject_button' in request.POST:
            request.session['tabactive'] = 'liPDCC'
            app.id_days_validation_state = State.objects.get(pk=3)
            app.save()
            if report_receive_form.is_valid():
                obs = report_receive_form.cleaned_data['obs']
                subject = "Solicitud Salida: Validacion de días Rechazada"
                message = "La solicitud de salida N°"+id_app+" ha sido rechazada por la jefa de dirección."
                if obs != "":
                    message += "\n\nSe agregó la siguiente observación:\n" + obs
                message += "\n\n-- Este correo fue generado automáticamente."
                send_mail(subject, message, settings.EMAIL_HOST_USER, { teacher.mail, EMAIL_MAGNA }, fail_silently = True)
                return redirect('list_angelica')
            else:
                print("report_receive_form invalid")
            return redirect('list_angelica')

    return render(request, 'Angelica/days_validation.html', locals()) #por algun motivo djanguistico misterioso esto funciona...
    #return render_to_response("Angelica/days_validation.html", locals(), content_type=RequestContext(request))

@csrf_protect
@login_required
def list_angelica(request):
    user = request.user
    apps = Application.objects.all()
    return render_to_response("Angelica/list_angelica.html", locals(), content_type=RequestContext(request))



@csrf_exempt
def contacto(request):
    form = contactoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            nombre=form.cleaned_data['nombre']
            mail=form.cleaned_data['email']
            asunto=form.cleaned_data['asunto']
            mensaje=form.cleaned_data['mensaje']
            send_mail(asunto, mensaje, settings.EMAIL_HOST,{mail,settings.EMAIL_HOST}, fail_silently = True)
            return redirect("login2")
    return  render_to_response("General/contacto.html", locals(), content_type=RequestContext(request))


@csrf_exempt
def acerca(request):
    return  render_to_response("General/about_us.html", locals(), content_type=RequestContext(request))
