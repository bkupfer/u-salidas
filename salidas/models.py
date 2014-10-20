from django.db import models
from django.utils.encoding import smart_text

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
    id_currency = models.ForeignKey('Currency')
    amount = models.PositiveIntegerField()
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


class CommissionType(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
       return self.type


class Application(models.Model):
    id_Teacher = models.ForeignKey('Teacher')
    id_commission_type = models.ForeignKey('CommissionType')
    motive = models.TextField()
    financed_by = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    id_days_validation_state = models.ForeignKey('State', related_name='+')  # (?) related name because related name
    id_funds_validation_state = models.ForeignKey('State')
    directors_name = models.CharField(max_length=30)
    directors_rut = models.CharField(max_length=10)
    def __str__(self):
        return "Application "+str(self.id)
    #Obtiene el ultimo estado asociado a la solicitud
    def get_state(self):
        try:
            ret = ApplicationHasApplicationState.objects.filter(id_application=self.pk).order_by("date").reverse()[0].id_application_state
        except:
            print("error en linea 68 del archivo models revisar get state")
            ret = "Estado vacío, revisar"
        return ret
    #Obtiene la fecha del envio a facultad
    def sent_date(self):
        state = ApplicationState.objects.get(pk=2)
        applicationState = ApplicationHasApplicationState.objects.filter(id_application=self.pk,id_application_state=state)
        try:
            ret = applicationState[0].date
          #  ret = applicationState.order_by("date").reverse()[0].date
        except:
            ret = "No enviada"
        return ret
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


class Teacher(models.Model):
    rut = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    signature = models.ImageField(max_length=255, blank=True, null=True, upload_to='signatures')
    profile_picture = models.URLField(blank=True, null=True)
    mail = models.EmailField()
    def __str__(self):
        return self.name + " " + self.last_name

#rut_teacher es un Teacher no un rut!!!
class Replacement(models.Model):
    rut_teacher = models.ForeignKey('Teacher')
    id_Application = models.ForeignKey('Application')
    answer_date = models.DateTimeField(blank=True, null=True)
    id_state = models.ForeignKey('State')


class State(models.Model):
    state = models.CharField(max_length=16)
    def __str__(self):
        return self.state


class InactivePeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()  # blank=True, null=True
    description = models.TextField(blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)
    section = models.IntegerField(max_length=2)
    def __str__(self):
        return self.name


class Module(models.Model):
    block = models.CharField(max_length=3)
    def __str__(self):
        return self.block


class CourseHasModule(models.Model):
    id_Course = models.ForeignKey('Course')
    id_Module = models.ForeignKey('Module')


class TeacherHasCourse(models.Model):
    id_Teacher = models.ForeignKey('Teacher')
    id_Course = models.ForeignKey('Course')

