from django.db import models
from django.utils.encoding import smart_text

# Create your models here.
class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=5)
class Finance_type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
class Finance(models.Model):
    id_application = models.ForeignKey('Application')
    id_finance_type = models.ForeignKey('Finance')
    id_currency = models.ForeignKey('Currency')
    amount = models.FloatField()
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100)
class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey('Country')
    city = models.CharField(max_length=100)
class Destination(models.Model):
    id_Application = models.ForeignKey('Application')
    id_city = models.ForeignKey('City')
    start_date = models.DateField()
    end_date = models.DateField()
class Commission_type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10)
    id_commission_type = models.ForeignKey('Commission_type')
    motive = models.TextField()#blank=True
    creation_date = models.DateTimeField()
    id_days_validation_state = models.ForeignKey('State', related_name='+' )#? related name porque si
    id_funds_validation_state = models.ForeignKey('State')
    directors_name = models.CharField(max_length=30)
    directors_rut = models.CharField(max_length=10)
class Application_state(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=20)
class Application_has_Application_state(models.Model):
    id_Application = models.ForeignKey('Application')
    id_Application_state = models.ForeignKey('Application_state')
    date =models.DateTimeField()
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(blank=True, null=True,max_length=200)
    id_application = models.ForeignKey('Application')
class Teacher(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    signature_path = models.CharField(max_length=100, blank=True, null=True)
class Replacement(models.Model):
    id = models.AutoField(primary_key=True)
    rut_teacher = models.ForeignKey('Teacher')
    id_Application = models.ForeignKey('Application')
    #id_curso
    answer_date = models.DateTimeField(blank=True, null=True)
    id_state = models.ForeignKey('State')
class State(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=30)
class inactive_period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()#blank=True, null=True
    description = models.TextField(blank=True, null=True)





class FormData(models.Model):
    # required
    #type_of_commision = models.CharField(max_length=120) # change to list
    A = 'Académica'
    E = 'Estudio'
    possible_commissions = (
                    (A, 'Académica'),
                    (E, 'Estudio'),)
    type_of_commission = models.CharField(max_length=2,
                                         name="Tipo de comisión",
                                         choices=possible_commissions,
                                         default=A)

    motive = models.TextField(max_length=100, name="Motivo")

    financed = models.CharField(max_length=120, name="Financiamiento")

    currency = models.CharField(max_length=3, name="Tipo de moneda")
    amount  = models.IntegerField()

    country = models.CharField(max_length=120, name="País de destino")
    city    = models.CharField(max_length=120, name="Ciudad de destino")

    departure_date  = models.DateTimeField()
    return_date     = models.DateField()

 #   signature = models.ImageField()
    substitute_teacher = models.CharField(max_length=120, name="Profesor substituto")

    # aditional info
    email       = models.EmailField()
    timestamp =  models.DateTimeField(auto_now_add=True, auto_now=False) # auto_now_add=True -> when created set time, auto_now=False -> when updated, don't change it

    def __str__(self):
        return smart_text(self.email)

