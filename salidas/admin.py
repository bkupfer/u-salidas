from django.contrib import admin

# Register your models here.
from . import models
'''
class CurrencyAdmin(admin.ModelAdmin):
    class Meta:
        model = Currency
'''
#admin.site.register(Currency, CurrencyAdmin)
admin.site.register(models.Currency)
admin.site.register(models.City)
admin.site.register(models.Country)
