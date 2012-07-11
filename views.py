#coding: utf-8
import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings

from log_analysis.log.models import Current
from log_analysis.forms import EditForm

class UploadFileForm(forms.Form):
    """Model of form for file upload"""
    file = forms.FileField()

def redirect(request):
    """Redirects to index site"""
    return HttpResponseRedirect("log_analysis/index")

def index(request):
    """Returns main site for log and text file analysis"""
    form = UploadFileForm()
    return render_to_response("index.html", {"form":form})

def data_view(request):
    """Returns view on current data ordered by count"""
    #terms = Current.objects.filter(count__gt = 6).order_by("-count")
    terms = Current.objects.all().order_by("-count")
    return render_to_response("data_view.html", {'terms': terms})

def data_edit(request):
    """Returns view on current data ordered by count"""
    #terms = Current.objects.filter(count__gt = 6).order_by("-count")
    edit_form = EditForm()
    terms = Current.objects.all().order_by("-count")
    return render_to_response("data_edit.html", {'terms': terms, "edit_form": edit_form})


#def getUnproccessedLogs():
        ##return [ (log, str(os.path.getsize(os.path.join(settings.ROOT, "static/logy", log))/1024) + " kB") for log in os.listdir(os.path.join(settings.ROOT, "static/logy")) if "log" in log]
        #return [ (log, str(os.path.getsize(os.path.join(settings.ROOT, "static/logy", log))/1024) + " kB") for log in os.listdir(os.path.join(settings.ROOT,
#"static/logy"))]
#def getArchiveFiles():
        #return [ archiveFile for archiveFile in os.listdir(os.path.join(settings.ROOT, "static/logy_csv")) ]