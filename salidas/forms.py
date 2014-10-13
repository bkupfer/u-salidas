from django import forms
from salidas.models import *
import datetime
from django.forms.models import inlineformset_factory,formset_factory

class NewApplicationForm(forms.ModelForm):
    rut = forms.CharField()
    commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),widget=forms.Select(attrs={'placeholder':u'Seleccione el tipo de comisión'}))
    motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))

    class Meta:
        model = Application
        exclude = ('id_days_validation_state', 'id_funds_validation_state','directors_name','directors_rut')
        #fields = ('motive','financed_by')

class DestinationForm(forms.ModelForm):
    country = forms.CharField(widget=forms.HiddenInput(attrs={'class':"hidden"}))
    city = forms.CharField(widget=forms.HiddenInput(attrs={'class':"hidden"}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    class Meta:
        model = Destination
        exclude = {'id'}

class ReplacementApplicationForm(forms.Form):
    teachers = forms.ModelChoiceField(queryset=Teacher.objects.all(),label='',widget=forms.Select(attrs={'placeholder':'Seleccione un Profesor'}))

DestinationFormSet = formset_factory(DestinationForm, extra=1)




