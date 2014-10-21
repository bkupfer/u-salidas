from django.contrib import admin

# Register your models here.
from . import models

#admin.site.register(Currency, CurrencyAdmin)
admin.site.register(models.Currency)
admin.site.register(models.FinanceType)
admin.site.register(models.Finance)
admin.site.register(models.Country)
admin.site.register(models.City)
admin.site.register(models.Destination)
admin.site.register(models.CommissionType)
admin.site.register(models.Application)
admin.site.register(models.ApplicationState)
admin.site.register(models.ApplicationHasApplicationState)
admin.site.register(models.Document)
admin.site.register(models.Teacher)
admin.site.register(models.Replacement)
admin.site.register(models.State)
admin.site.register(models.InactivePeriod)
admin.site.register(models.Course)
admin.site.register(models.CourseHasModule)
admin.site.register(models.Module)
admin.site.register(models.TeacherHasCourse)
admin.site.register(models.ReplacementType)