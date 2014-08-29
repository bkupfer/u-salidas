from django.db import models
from django.utils.encoding import smart_text

# Create your models here.
class FormData(models.Model):
    # required
    type_of_commision = models.CharField(max_length=120) # change to list
    motive = models.TextField(max_length=500)
    financed_by = models.CharField(max_length=120)
    amount = models.IntegerField()
    destiny_country = models.CharField(max_length=120)
    destiny_city = models.CharField(max_length=120)
    departure_date = models.DateField()
    return_date = models.DateField()
 #   signature = models.ImageField()
    substitue_techaer = models.CharField(max_length=120)

    # aditional info
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False) # auto_now_add=True -> when created set time, auto_now=False -> when updated, don't change it

    def __str__(self):
        return smart_text(self.email)

