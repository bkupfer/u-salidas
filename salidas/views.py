from django.shortcuts import render, render_to_response, RequestContext

from salidas.forms import *

# Create your views here.
def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))

def new_application(request):
    application = NewApplicationForm(request.POST or None)
    destination = DestinationFormSet(request.POST or None)
    if application.is_valid():
        save_it = application.save(commit=False)
        save_it.save()
    if destination.is_valid():
        save_it = destination.save(commit=False)
        save_it.save()
    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))


