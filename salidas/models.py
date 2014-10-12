from django.db import models
from django.utils.encoding import smart_text

#Las funciones  de __str__ son el nombre con el que se representan en la pantalla de admin las filas de las tablas, por defecto diria
#"[Tabla.name] object"
class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=4)

    def __str__(self):
       return self.currency


class FinanceType(models.Model):
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

    def __str__(self):
       return self.country


class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey('Country')
    city = models.CharField(max_length=100)

    def __unicode__(self):
       return self.city


class Destination(models.Model):
    id_Application = models.ForeignKey('Application')
    #  id_city = models.ForeignKey('City')
    country = models.CharField(max_length=30)
    city    = models.CharField(max_length=30)
    start_date = models.DateField(name="Fecha de Inicio")
    end_date   = models.DateField(name="Fecha de Término")

class CommissionType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)

    def __str__(self):
        return smart_text(self.type)


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10)
    id_commission_type = models.ForeignKey('CommissionType', name="Tipo de comisión")
    motive = models.TextField(name="Motivo")
    financed_by = models.TextField(name="Financiado por")
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    id_days_validation_state = models.ForeignKey('State', related_name='+')  # (?) related name because related name
    id_funds_validation_state = models.ForeignKey('State')
    directors_name = models.CharField(max_length=30)
    directors_rut = models.CharField(max_length=10)


class ApplicationState(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=20)


class ApplicationHasApplicationState(models.Model):
    id_Application = models.ForeignKey('Application')
    id_Application_state = models.ForeignKey('ApplicationState')
    date = models.DateTimeField()


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(blank=True, null=True, max_length=200)
    id_application = models.ForeignKey('Application')


class Teacher(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    signature_path = models.CharField(max_length=100, blank=True, null=True)


class Replacement(models.Model):
    id = models.AutoField(primary_key=True)
    rut_teacher = models.ForeignKey('Teacher')
    id_Application = models.ForeignKey('Application')
    #id_curso  // revisar si este campo es necesario - depende de los datos provistos por u-pasaporte.
    answer_date = models.DateTimeField(blank=True, null=True)
    id_state = models.ForeignKey('State')


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=16)


class InactivePeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()  # blank=True, null=True
    description = models.TextField(blank=True, null=True)



'''
Old example of a django form;

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

'''
