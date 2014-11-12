# -*- coding: utf-8 -*-
from django import forms
from salidas.models import *
from django.forms.models import inlineformset_factory, formset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

# New application form
class NewApplicationForm(forms.ModelForm):
    id_commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),
                                                empty_label="Seleccione Tipo de Comisión")
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
    #id_finance_type = forms.ModelChoiceField(queryset=FinanceType.objects.all(),empty_label="tipo de financiamiento")
    class Meta:
        model = Finance
        exclude = {'id_application','id_finance_type'}


class FinanceDccForm(FinanceForm):
    checkbox = forms.BooleanField(required=True, label="Chequéate esta buey")


FinanceFormSet = formset_factory(FinanceDccForm, extra=3)
FinanceFormSet_Edit= formset_factory(FinanceDccForm,extra=0)


class DestinationForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(
        attrs={'onchange': "print_state('state',this.selectedIndex, this.id);updateCountryTxt(this);"}))
    city = forms.CharField(widget=forms.Select(attrs={'class': 'city', 'onchange': "updateStateTxt(this);"},
                                               choices=([("", "Seleccione Ciudad")])))
    start_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  #
    end_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  # widget=SelectDateWidget()

    class Meta:
        model = Destination
        exclude = {'application'}


DestinationFormSet = formset_factory(DestinationForm, extra=1)
DestinationFormSet_Edit = formset_factory(DestinationForm, extra=0)


class AcademicReplacementApplicationForm(forms.Form):

    acteachers = forms.ModelChoiceField(queryset=Teacher.objects.none(),widget=forms.Select(attrs={'placeholder':'Seleccione un Profesor'}))

    def __init__(self,*args,**kwargs):
        user=args[1].id
        super(AcademicReplacementApplicationForm,self).__init__()
        try:
            initial=kwargs['initial']
            print(initial)
        except:
            initial=None
        self.fields['acteachers'].queryset =Teacher.objects.exclude(user=user)
        self.fields['acteachers'].initial = initial


class ReplacementApplicationForm(forms.Form):

    repteachers = forms.ModelChoiceField(queryset=Teacher.objects.none(),widget=forms.Select(attrs={'placeholder':'Seleccione un Profesor'}))

    def __init__(self,*args,**kwargs):
        super(ReplacementApplicationForm,self).__init__()
        print(args)
        print(kwargs)
        try:
            initial=kwargs['initial']
            print(initial)
        except:
            initial=None
        user=args[1].id
        try:
            teacher1=Teacher.objects.get(user=user)
            y_modules=teacher1.get_modules()
            my_modules=set(y_modules)
            teachers = Teacher.objects.all().exclude(user=user)
            query=teachers
            for teacher in teachers:
                their_modules=set(teacher.get_modules())
                if not my_modules.isdisjoint(their_modules):
                    #print(query)
                    query=query.exclude(id=teacher.id)
        except TeacherHasCourse.DoesNotExist:
            query=Teacher.objects.all()

        self.fields['repteachers'].queryset = query
        self.fields['repteachers'].initial = initial

class DocumentForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Document
        exclude = {'id_application', 'path'}


DocumentFormSet = formset_factory(DocumentForm, extra=1)
DocumentFormSet_Edit = formset_factory(DocumentForm, extra=0)

# My information form
class MyInformation(forms.Form):
    email = forms.EmailField()
    jornada = forms.ModelChoiceField(queryset=WorkingDay.objects.all(), empty_label="Seleccione tipo de jornada")

class TeachersSignature2(forms.Form):
    sign = forms.ImageField()


class TeacherSignature(forms.ModelForm):
    signature = forms.ImageField()
    class Meta:
        model = Teacher
        exclude = {'rut', 'name', 'last_name', 'profile_picture = models.URLField()', 'mail'}

class stateForm(forms.Form):
    state=forms.ModelChoiceField(queryset=ApplicationState.objects.all())
