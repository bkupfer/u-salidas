from django import forms
from salidas.models import *
import datetime
from django.forms.models import inlineformset_factory,formset_factory

class NewApplicationForm(forms.ModelForm):
    motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))

    class Meta:
        model = Application
        fields = ('motive','financed_by')


class CommissionTypeForm(forms.Form):
    commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all())

class DestinationForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today)
    class Meta:
        model = Destination
        exclude = {'id_Application'}



