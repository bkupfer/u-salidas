from django.shortcuts import render, render_to_response, RequestContext
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.contrib.auth import  authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.urlresolvers import reverse
from salidas.forms import *
from io import StringIO
#from docx import * #to generate Docs
import io,os,os.path,tempfile, zipfile

def getfiles(request):
    id_app = request.GET['id']
    app = Application.objects.get(pk = id_app)
    path1 = solicitud_facultad_doc(app)
    path2 = peticion_docente_doc(app)
    # Files (local path) to put in the .zip
    filenames = [path1, path2]

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    zip_subdir = "documentos"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    f = io.BytesIO()
    # The zip compressor
    zf = zipfile.ZipFile(f, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(f.getvalue(),content_type='application/zip')
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

def peticion_docente_doc(app):
    # user = request.user.id
    document = Document()
    document.add_paragraph("Eric Tanter").alignment = 2 #
    document.add_paragraph("DCC - UChile").alignment = 2
    document.add_paragraph("etanter@dcc.uchile.cl").alignment = 2
    p = document.add_paragraph()
    p.add_run().add_break()
    p.add_run('Señor ').bold = True
    p.add_run().add_break()
    p.add_run('Sergio Ochoa').bold = True
    p.add_run().add_break()
    p.add_run('Director DCC').bold = True
    p.add_run().add_break()
    p.add_run('Presente').bold = True
    p.add_run().add_break()

    path = os.path.join(settings.MEDIA_ROOT, 'carta_peticion_docente.docx') #todo:path para cada profe (?)
    document.save(path)
    return path

def solicitud_facultad_doc(app):
    document = Document()
    title = document.add_paragraph('SOLICITUD DE COMISION O PERMISO')
    title.alignment = 1
    p = document.add_paragraph()
    run = p.add_run()
    run.add_break()
    p.add_run('UNIDAD ACADEMICA ').bold = True
    p.add_run('     DEPARTAMENTO DE CIENCIAS DE LA COMPUTACION')
    path = os.path.join(settings.MEDIA_ROOT, 'solicitud_facultad.doc')
    document.save(path)
    return path
