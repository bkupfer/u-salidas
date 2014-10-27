from django import forms
from salidas.models import *
import datetime
from django.forms.models import inlineformset_factory, formset_factory
from django.forms.extras.widgets import SelectDateWidget


class NewApplicationForm(forms.ModelForm):
    id_commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),
                                                empty_label="Seleccione Tipo de Comisión")  #
    motive = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Fundamentos'}))
    financed_by = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Indique quien financia...'}))

    class Meta:
        model = Application
        exclude = (
            'id_Teacher', 'directors_name', 'directors_rut', 'id_days_validation_state', 'id_funds_validation_state')
        # fields = ('motive','financed_by')


class FinanceForm(forms.ModelForm):
    id_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="Tipo de Moneda")
    amount = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'placeholder': u'  Ingrese un Monto...'}))

    class Meta:
        model = Finance
        exclude = {'id_application', 'id_finance_type'}


class FinanceDccForm(FinanceForm):
    checkbox = forms.BooleanField(required=True, label="Chequéate esta buey")


FinanceFormSet = formset_factory(FinanceDccForm, extra=3)


class DestinationForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(
        attrs={'onchange': "print_state('state',this.selectedIndex, this.id);updateCountryTxt(this);"}))
    city = forms.CharField(widget=forms.Select(attrs={'class': 'city', 'onchange': "updateStateTxt(this);"},
                                               choices=([("", "Seleccione Ciudad")])))
    start_date = forms.DateField(input_formats=['%d/%m/%y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yy"}))  #
    end_date = forms.DateField(input_formats=['%d/%m/%y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yy"}))  # widget=SelectDateWidget()

    class Meta:
        model = Destination
        exclude = {'application'}


DestinationFormSet = formset_factory(DestinationForm, extra=1)


class ReplacementApplicationForm(forms.Form):
    teacher = Teacher.objects.get(pk=1)
    achoices = teacher.get_possible_replacement_teachers()
    teachers = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'Seleccione un Profesor'}), choices=achoices)


class AcademicReplacementApplicationForm(forms.Form):
    teacher = Teacher.objects.get(pk=1)
    all = Teacher.objects.all()
    teachers = forms.ModelChoiceField(queryset=all.exclude(pk=teacher.pk),widget=forms.Select(attrs={'placeholder':'Seleccione un Profesor'}))



class DocumentForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Document
        exclude = {'id_application', 'path'}


DocumentFormSet = formset_factory(DocumentForm, extra=1)


class TeacherSignatureForm(forms.ModelForm):
    signature = forms.ImageField()

    class Meta:
        model = Teacher
        exclude = {'rut', 'name', 'last_name', 'profile_picture = models.URLField()', 'mail'}
