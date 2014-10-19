from django import forms
from salidas.models import *
import datetime
from django.forms.models import inlineformset_factory,formset_factory

class NewApplicationForm(forms.ModelForm):
    id_commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),widget=forms.Select(attrs={'placeholder':u'Seleccione el tipo de comisión'}))
    motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))
    class Meta:
        model = Application
        exclude = ('id_Teacher','directors_name','directors_rut','id_days_validation_state','id_funds_validation_state')
        #fields = ('motive','financed_by')

class FinanceForm(forms.ModelForm):
    id_currency = forms.ModelChoiceField(queryset=Currency.objects.all(),widget=forms.Select(attrs={'placeholder':u'Tipo de moneda'}))
    checkbox = forms.BooleanField(label="Chequéate esta buey")
    class Meta:
        model = Finance
        exclude = {'id_application' , 'id_finance_type'}

class DestinationForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(attrs={'onchange':"print_state('state',this.selectedIndex, this.id);updateCountryTxt(this);"}))
    city = forms.CharField(widget=forms.Select(attrs={'onchange':"updateStateTxt(this);"}, choices=([("seleccione ciudad", "seleccione ciudad")])))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    class Meta:
        model = Destination
        exclude = {'application'}

class ReplacementApplicationForm(forms.Form):
    teachers = forms.ModelChoiceField(queryset=Teacher.objects.all(),widget=forms.Select(attrs={'placeholder':'Seleccione un Profesor'}))

DestinationFormSet = formset_factory(DestinationForm, extra=1)





