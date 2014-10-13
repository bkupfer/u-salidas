from django.shortcuts import render, render_to_response, RequestContext

from salidas.forms import *

# Create your views here.
def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))

def new_application(request):
    application = NewApplicationForm(request.POST or None)
    destinationFormSet = DestinationFormSet(request.POST or None)
    if application.is_valid():
        new_app = application.save(commit=False)
        new_app.save()
    if destinationFormSet.is_valid():
        new_destination = destinationFormSet.save(commit=False)
        new_destination.save()
    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))


def application_detail(request):
    CommissionType.objects
    b = CommissionType(pk=1)
    return render_to_response("application_detail.html", locals(), context_instance=RequestContext(request))


def teacher_calendar(request):
    return render_to_response("teacher_calendar.html", locals(), context_instance=RequestContext(request))
