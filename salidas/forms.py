from django import forms
from salidas.models import *
from django.forms.models import inlineformset_factory,formset_factory

class NewApplicationForm(forms.ModelForm):
    motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))

    class Meta:
        model = Application
        fields = ('motive','financed_by')


class CommissionTypeForm(forms.Form):
    commission_type = forms.ModelChoiceField(queryset=Commission_type.objects.all())
