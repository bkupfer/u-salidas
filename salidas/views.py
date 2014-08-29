from django.shortcuts import render, render_to_response, RequestContext

from .new_application import NewApplicationForm

# Create your views here.
def home(request):
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))

def new_application(request):
    form = NewApplicationForm(request.POST or None)

    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()

    return render_to_response("new_application_form.html", locals(), context_instance=RequestContext(request))

