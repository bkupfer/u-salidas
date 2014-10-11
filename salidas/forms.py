from django import forms
from salidas.models import *
import datetime
from django.forms.models import inlineformset_factory,formset_factory

class NewApplicationForm(forms.ModelForm):
   # motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    #financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))

    class Meta:
        model = Application
        exclude = ('id_days_validation_state', 'id_funds_validation_state','rut','directors_name','directors_rut')
        #fields = ('motive','financed_by')

class DestinationForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today)
    country = forms.CharField(widget=forms.HiddenInput(attrs={'class':"hidden"}))
    city = forms.CharField(widget=forms.HiddenInput(attrs={'class':"hidden"}))
    class Meta:
        model = Destination
        exclude = {'id_Application'}


DestinationFormSet = formset_factory(DestinationForm, extra=1)



