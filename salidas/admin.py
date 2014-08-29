from django.contrib import admin

# Register your models here.
from .models import FormData

class FormDataAdmin(admin.ModelAdmin):
    class Meta:
        model = FormData

admin.site.register(FormData, FormDataAdmin)