from django.db import models
from django.utils.encoding import smart_text

# Create your models here.
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

