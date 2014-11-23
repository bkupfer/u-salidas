# -*- coding: utf-8 -*-
from django import forms
from salidas.models import *
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

# New application form
class NewApplicationForm(forms.ModelForm):
    id_commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),
                                                empty_label="Seleccione Tipo de Comisión",
                                                widget=forms.Select(attrs={'class':'form-control input-sm'}))
    class Meta:
        model = Application
        exclude = (
            'id_Teacher', 'directors_name', 'directors_rut', 'id_days_validation_state', 'id_funds_validation_state')
        # fields = ('motive','financed_by')

class NewApplicationFormEdit(forms.ModelForm):
    id_commission_type = forms.ModelChoiceField(queryset=CommissionType.objects.all(),
                                                empty_label="Seleccione Tipo de Comisión",
                                                widget=forms.Select(attrs={'class':'form-control input-sm'}))
    directors_name = forms.CharField()
    class Meta:
        model = Application
        exclude = (
            'id_Teacher', 'directors_rut', 'id_days_validation_state', 'id_funds_validation_state')
        # fields = ('motive','financed_by')
class FinanceForm(forms.ModelForm):
    id_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label="Moneda",
                                         widget=forms.Select(attrs={'class':'form-control input-sm'}))
    amount = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class':'form-control input-sm','placeholder': u'  Ingrese un Monto...'}))
    financed_by = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':"form-control",
                                                                'placeholder': u'Ej: "Conicyt - Fondecyt #1120207"'}))

    #financed_by_dcc = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    #id_finance_type = forms.ModelChoiceField(queryset=FinanceType.objects.all(),empty_label="tipo de financiamiento")
    class Meta:
        model = Finance
        exclude = {'id_application','id_finance_type'}


# class FinanceDccForm(FinanceForm):
#     checkbox = forms.BooleanField(required=True, label="Chequéate esta buey")

FinanceFormSet = formset_factory(FinanceForm, max_num=3, extra=3)
FinanceFormSet_Edit= formset_factory(FinanceForm,extra=0)


class DestinationForm(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(
        attrs={'class': 'form-control input-sm','onchange': "print_state('state',this.selectedIndex, this.id);"}))
    city = forms.CharField(widget=forms.Select(attrs={'class': 'city form-control input-sm'},
                                               choices=([("", "Seleccione Ciudad")])))
    start_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  #
    end_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  # widget=SelectDateWidget()
    motive = forms.CharField( max_length = 500,widget=forms.Textarea(attrs={'placeholder': u'Ej: "Participaré en las actividades del proyecto PRADESC, a través del cual nuestro departamento está colaborando con diversas organizaciones alemanas, en particular participaré en actividades que se refieren al desarrollo de soluciones inteligentes para apoyar sistemas urbanos."'}))
    class Meta:
        model = Destination
        exclude = {'application'}

class DestinationFormEdit(forms.ModelForm):
    country = forms.CharField(widget=forms.Select(
        attrs={'class': 'form-control input-sm'}))
    city = forms.CharField(widget=forms.Select(attrs={'class': 'city form-control input-sm'},
                                               choices=([("", "Seleccione Ciudad")])))
    start_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  #
    end_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy", 'onchange': "count_avaliable_days(this);"}))  # widget=SelectDateWidget()
    motive = forms.CharField( max_length = 500,widget=forms.Textarea(attrs={'placeholder': u'Ej: "Participaré en las actividades del proyecto PRADESC, a través del cual nuestro departamento está colaborando con diversas organizaciones alemanas, en particular participaré en actividades que se refieren al desarrollo de soluciones inteligentes para apoyar sistemas urbanos."'}))
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
        except:
            initial=None
        user=args[1].id
        try:
            teacher1=Teacher.objects.get(user=user)
            y_modules=teacher1.get_modules()
            my_modules=set(y_modules)
            y_courses=teacher1.get_courses()
            my_courses=set(y_courses)
            teachers = Teacher.objects.all().exclude(user=user)
            query=teachers
            for teacher in teachers:
                their_courses=set(teacher.get_courses())
                diff_courses= their_courses.difference(my_courses)
                #su horario sin contar los ramos comunes
                their_modules = []
                for course in diff_courses:
                    their_modules+=(course.get_modules())
                #si tienen topes lo saco de la lista
                if not my_modules.isdisjoint(their_modules):
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


class contactoForm(forms.Form):
    nombre = forms.CharField(40)
    email = forms.EmailField()
    asunto = forms.CharField(20)
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': u'Comentarios, sugerencias o errores...'}))


class ReportReceiveForm(forms.Form):
    send_date = forms.DateField(input_formats=['%d/%m/%y', '%d/%m/%Y'], required=False, widget=forms.DateInput(
        attrs={'class': 'datepicker', 'data-date-format': "dd/mm/yyyy"}))
    obs = forms.CharField(max_length = 500, required=False, widget=forms.Textarea(attrs={'placeholder': u'Observaciones'}))

class RejectObservationsForm(forms.Form):
    obs = forms.CharField(max_length = 500, required=False, widget=forms.Textarea(attrs={'placeholder': u'Observaciones'}))