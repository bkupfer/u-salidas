from django.contrib import admin

# Register your models here.
from .models import *

class CurrencyAdmin(admin.ModelAdmin):
    class Meta:
        model = Currency

admin.site.register(Currency, CurrencyAdmin)