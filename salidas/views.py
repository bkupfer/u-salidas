from django.shortcuts import render, render_to_response, RequestContext

from .new_application import NewApplicationForm

# Create your views here.
def home(request):
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))

def index(request):
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))

def new_application(request):
    form = NewApplicationForm(request.POST or None)

    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()

    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))

def days_validation(request):
    return render_to_response("days_validation.html", locals(), context_instance=RequestContext(request))

def finance_validation(request):
    return render_to_response("finance_validation.html", locals(), context_instance=RequestContext(request))

def application_detail(request):
    return render_to_response("application_detail.html", locals(), context_instance=RequestContext(request))

def replacement_commitment(request):
    return render_to_response("replacement_commitment.html", locals(), context_instance=RequestContext(request))

