from django import forms

from .models import FormData

class NewApplicationForm(forms.ModelForm):
    class Meta:
        model = FormData