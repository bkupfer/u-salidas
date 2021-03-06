# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from datetime import date
from django.utils.encoding import smart_text
from datetime import datetime
#Las funciones  de __str__ son el nombre con el que se representan en la pantalla de admin las filas de las tablas, por defecto diria
#"[Tabla.name] object"
class Currency(models.Model):
    currency = models.CharField(max_length=4)
    def __str__(self):
       return self.currency


class FinanceType(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
        return self.type


class Finance(models.Model):
    id_application = models.ForeignKey('Application')
    id_finance_type = models.ForeignKey('FinanceType')
    #financed_by_dcc = models.BooleanField(default=False)
    id_currency = models.ForeignKey('Currency',blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    financed_by = models.TextField(blank=True, null=True)
    def get_finance_type(self):
        return self.id_finance_type.type


class Country(models.Model):
    country = models.CharField(max_length=100)
    def __str__(self):
       return self.country


class City(models.Model):
    country = models.ForeignKey('Country')
    city = models.CharField(max_length=100)
    def __str__(self):
       return self.city


class Destination(models.Model):
    application = models.ForeignKey('Application')
    country = models.CharField(max_length=55)
    city    = models.CharField(max_length=55)
    start_date = models.DateField()
    end_date   = models.DateField()
    motive = models.TextField()

    def get_used_days(self):
        dt = self.end_date - self.start_date
        return dt.days


class CommissionType(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
       return self.type


class Application(models.Model):
    id_Teacher = models.ForeignKey('Teacher')
    id_commission_type = models.ForeignKey('CommissionType')
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    id_days_validation_state = models.ForeignKey('State', related_name='+')  # (?) related name because related name
    id_funds_validation_state = models.ForeignKey('State')
    directors_name = models.CharField(max_length=50)
    directors_rut = models.CharField(max_length=10)
    used_days = models.FloatField(null=True, blank=True)
    def __str__(self):
        return "Application "+str(self.id)

    #Obtiene el ultimo estado asociado a la solicitud
    def get_state(self):
        try:
            ret = ApplicationHasApplicationState.objects.filter(id_application=self.pk).order_by("date").reverse()[0].id_application_state
        except:
            print("Error in method get_state(). (models.py, Application)")
            ret = "Estado vacío, revisar"
        return ret

    #Obtiene la fecha del envio a facultad
    def sent_date(self):
        state = ApplicationState.objects.get(pk=3)
        applicationState = ApplicationHasApplicationState.objects.filter(id_application=self.pk,id_application_state=state)
        try:
            #ret = applicationState[1].date
            ret = applicationState.order_by("date").reverse()[0].date
        except:
            ret = "No enviada"
        return ret

    def get_destinations(self):
        dests = Destination.objects.filter(application=self)
        return dests

    def get_used_days(self):
        return self.used_days

    def compute_used_days(self):
        dests = self.get_destinations()
        computed_days = 0
        for dest in dests:
            computed_days += dest.get_used_days()
        if computed_days < 0:
            return 0
        return computed_days

    def get_documents(self):
        docs = Document.objects.filter(id_application=self)
        return docs

    def get_replacements(self):
        replacements = Replacement.objects.filter(id_Application = self)
        return replacements

    def discount_days(self):
        if self.id_commission_type == CommissionType.objects.get(type="Academica") and self.get_state() != State.objects.get(pk=3):
            return True
        return False

    def get_finances(self):
        finances=Finance.objects.filter(id_application=self)
        return finances

    def get_start_date(self):
        dests=self.get_destinations()
        start_date=date.max
        for dest in dests:
            if dest.start_date<start_date:
                start_date=dest.start_date
        return start_date

    def get_end_date(self):
        dests=self.get_destinations()
        end_date=date.min
        for dest in dests:
            if dest.end_date>end_date:
                end_date=dest.end_date
        return end_date

    def get_week_days_missed(self):
        destinations = self.get_destinations()
        week_days_missed = dict()
        for destination in destinations:
            start_date=destination.start_date
            end_date=destination.end_date
            for date in range(start_date,end_date):
                #TODO inactive days
                week_days_missed[str(datetime.weekday(date))] += 1
        return week_days_missed

    def get_replacement_state(self):
        replacements = Replacement.objects.get(id_Application=self,type=1)
        return replacements.get_state()

    def get_academic_replacement_state(self):
        replacements = Replacement.objects.get(id_Application=self,type=2)
        return replacements.get_state()


class ApplicationState(models.Model):
    state = models.CharField(max_length=20)
    def __str__(self):
        return self.state


class ApplicationHasApplicationState(models.Model):
    id_application = models.ForeignKey('Application')
    id_application_state = models.ForeignKey('ApplicationState')
    date = models.DateTimeField(auto_now_add=True, auto_now=False)


class Document(models.Model):
    id_application = models.ForeignKey('Application')
    file = models.FileField(blank=True, null=True,upload_to='documents')


 #jornada:parcial -> jerarquia: profesor adjunto, jornada completa -> jerarquia : profesor asistente,asociado o titular
class Hierarchy(models.Model):
    hierarchy = models.CharField(max_length=20)
    avaliable_days = models.IntegerField()
    def __str__(self):
        return self.hierarchy


class WorkingDay(models.Model):
    working_day=models.CharField(max_length=30)
    def __str__(self):
        return self.working_day


class Teacher(models.Model):
    user = models.OneToOneField(User)
    rut = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    signature = models.ImageField(max_length=255, blank=True, null=True, upload_to='signatures')
    mail = models.EmailField() # todo: refactor to 'email' instead of 'mail'
    hierarchy = models.ForeignKey('Hierarchy')      # jerarquia docente; Asistente(1), Asociado(2), Instructor(3)
    working_day=models.ForeignKey('WorkingDay')     # jornada docente: Completa(1) Media (2)

    def __str__(self):
        return self.name + " " + self.last_name

    def get_courses(self):
        his_courses = TeacherHasCourse.objects.filter(id_Teacher=self) # todo: falta filtrar por semestre
        #if len(his_courses)==1:
        #    his_courses=[his_courses]
        courses = []
        for course in his_courses:
            courses=courses+[course.id_Course]
        return courses

    def get_modules(self):
        courses = self.get_courses()
        modules = []
        for course in courses:
            modules+=(course.get_modules())
        return modules
    def get_courses_with_modules(self):
        courses = self.get_courses()
        course_module= []
        for course in courses:
            course_module+=(course,course.get_modules())
        #convertir la lista de cursos-modulos en un diccionario
        course_module =dict(course_module[i:i+2] for i in range(0, len(course_module), 2))
        return course_module

    def get_applications(self):
        his_applications = Application.objects.filter(id_Teacher=self)
        return his_applications

    def get_used_days(self):
        his_apps = self.get_applications()
        used_days = 0
        for app in his_apps:
            if app.discount_days() and app.get_used_days() != None:
                tmonth = date.today().month  # todo: contar desde marzo a marzo
                tyear = date.today().year
                if app.get_start_date().year == tyear:
                    used_days += app.get_used_days()
        return used_days

    def get_avaliable_days(self):
        used_days = self.get_used_days()
        print(used_days)
        print(self.hierarchy.avaliable_days)
        return self.hierarchy.avaliable_days - used_days

    def get_used_academic_days(self):
        his_apps = self.get_applications()
        used_days = 0
        for app in his_apps:
            if app.discount_days() and app.get_used_days() != None:
                second_semester_month = 8 # april
                if date.today().month < second_semester_month: # primer semestre
                    if app.get_start_date().year == date.today().year and app.get_start_date().month < second_semester_month:
                        used_days += app.get_used_days()
                else:
                    if app.get_start_date().year == date.today().year and app.get_start_date().month >= second_semester_month:
                        used_days += app.get_used_days()
        return used_days

    def get_used_academic_weeks(self):
        return int(self.get_used_academic_days() / 7)

    def get_possible_replacement_teachers(self):
        y_modules = self.get_modules()
        my_modules = set(y_modules)
        replacement = [('','---------')]
        teachers = Teacher.objects.all().exclude(pk=self.pk)
        i=1
        for teacher in teachers:
            their_modules=set(teacher.get_modules())
            if my_modules.isdisjoint(their_modules):
                replacement.append((teacher.pk,teacher))
                i+=1
        return replacement
    def get_modules_with_collision(self):
        y_modules = self.get_modules()
        my_modules = set(y_modules)
        modules=[]
        teachers = Teacher.objects.all().exclude(pk=self.pk)
        for teacher in teachers:
            their_modules=set(teacher.get_modules())
            if not my_modules.isdisjoint(their_modules):
                for my_module in my_modules:
                    modules.append(my_module)
        modules = set(modules)
        return modules


    def get_teaching_weeks_by_course(self):
        his_applications=Application.objects.filter(id_Teacher=self)
        week_days_missed=dict()
        for application in his_applications:#por cada solicitud cuento cuantos lunes falte y cuántos martes y etc
            this_days_missed=application.get_week_days_missed()
            for day in week_days_missed:
                week_days_missed[day]+=this_days_missed[day]
        his_courses = TeacherHasCourse.objects.filter(id_Teacher=self)
        weeks_by_course=dict()
        for course in his_courses.id_Course:
            course_modules=course.get_modules()
            for module in course_modules:
                week_day=module.get_week_day()
                if week_days_missed[week_day]>0:
                    if course.get_ud == 5:
                        weeks_by_course[str(course)]+=1
                    elif course.get_ud == 10:
                        weeks_by_course[str(course)]+=0.5
                    else:
                        print("curso de uds raras")
        return weeks_by_course
    def get_working_day(self):
        return self.working_day.working_day



class Replacement(models.Model):
    rut_teacher = models.ForeignKey('Teacher')
    id_Application = models.ForeignKey('Application')
    answer_date = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('ReplacementType')
    id_state = models.ForeignKey('State')

    def get_appliant_teacher(self):
        return self.id_Application.id_Teacher
    def get_state(self):
        return self.id_state
    def get_start_date(self):
        return self.id_Application.get_start_date()
    def get_end_date(self):
        return self.id_Application.get_end_date()
    def get_courses(self):
        #reemplazo academico
        if self.type == ReplacementType.objects.get(pk=2):
            return None
        else:
            return self.id_Application.id_Teacher.get_courses()


class State(models.Model):
    state = models.CharField(max_length=16)
    def __str__(self):
        return self.state


class InactivePeriod(models.Model):
    start_date = models.DateField()
    end_date   = models.DateField()  # blank=True, null=True
    description = models.TextField(blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)
    section = models.IntegerField(max_length=2)
    year = models.IntegerField(max_length=4)
    semester = models.IntegerField(max_length=8)
    def __str__(self):
        return self.name
    def get_modules(self):
        its_modules = CourseHasModule.objects.filter(id_Course=self)
        modules=[]
        for module in its_modules:
            modules=modules+[module.id_Module]
        return modules


class Module(models.Model):
    block = models.CharField(max_length=3)
    def __str__(self):
        return self.block
    def get_week_day(self):
        weekDict={1:'Lunes', 2:'Martes', 3:'Miercoles', 4:'Jueves', 5:'Viernes', 6:'Sábado', 7:'Domingo'}
        return weekDict[self.get_week_day_number()]
    def get_week_day_number(self):
        return int(str(self.block).split('.')[0])
    def get_module_number(self):
        return int(str(self.block).split('.')[1])
    def get_start_time(self):
        start_timeDict={1:'08:30:00', 2:'10:15:00', 3:'12:00:00', 4:'14:30:00', 5:'16:15:00', 6:'18:00:00', 7:'19:45:00', 8:'21:15:00'}
        return start_timeDict[self.get_module_number()]
    def get_end_time(self):
        end_timeDict={1:'10:00:00', 2:'11:45:00', 3:'13:30:00', 4:'16:00:00', 5:'17:45:00', 6:'19:30:00', 7:'21:00:00', 8:'22:45:00'}
        return end_timeDict[self.get_module_number()]

class CourseHasModule(models.Model):
    id_Course = models.ForeignKey('Course')
    id_Module = models.ForeignKey('Module')


class TeacherHasCourse(models.Model):
    id_Teacher = models.ForeignKey('Teacher')
    id_Course = models.ForeignKey('Course')
    def __str__(self):
        return str(self.id_Teacher) + str("/")+ str(self.id_Course)


class ReplacementType(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
        return self.type

class admi(models.Model):
    user = models.CharField(max_length=20,)
    hash = models.CharField(max_length=100)

class SystemInformation(models.Model):
    director = models.CharField(max_length=50,default='')
    current_semester = models.IntegerField(max_length=1,default=0)
    current_year = models.IntegerField(max_length=4,default=0)
