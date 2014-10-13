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


class Finance(models.Model):
    id_application = models.ForeignKey('Application')
    id_finance_type = models.ForeignKey('Finance')
    id_currency = models.ForeignKey('Currency')
    amount = models.FloatField()


class Country(models.Model):
    country = models.CharField(max_length=100)


class City(models.Model):
    country = models.ForeignKey('Country')
    city = models.CharField(max_length=100)


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
    rut = models.CharField(max_length=10)
    id_commission_type = models.ForeignKey('CommissionType')    #, name="Tipo de comisión")
    motive = models.TextField()                                 # name="Motivo")
    financed_by = models.TextField()                            # name="Financiado por")
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    id_days_validation_state = models.ForeignKey('State', related_name='+')  # (?) related name because related name
    id_funds_validation_state = models.ForeignKey('State')
    directors_name = models.CharField(max_length=30)
    directors_rut = models.CharField(max_length=10)


class ApplicationState(models.Model):
    state = models.CharField(max_length=20)
    def __str__(self):
        return self.state


class ApplicationHasApplicationState(models.Model):
    id_application = models.ForeignKey('Application')
    id_application_state = models.ForeignKey('ApplicationState')
    date = models.DateTimeField()


class Document(models.Model):
    path = models.CharField(blank=True, null=True, max_length=200)
    id_application = models.ForeignKey('Application')


class Teacher(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    signature_path = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name + self.last_name


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
