#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from upload_data import upload
from django.conf import settings
from log_analysis.log.models import Current, Category, SubjectCategory
import os, datetime, csv

def store_updated_row(request):
    try:
        subject = request.POST["subject"]
        category = request.POST["category"]
        subject_category = request.POST["subject_category"]
        note = request.POST["note"]

        if "acquisition" in request.POST.keys():
            acquisition = 1
        else:
            acquisition = 0

        if int(category):
            category = Category.objects.get(categoryid = category)
            processed = 1
        else:
            category = None
            processed = 0

        if int(subject_category):
            subject_category = SubjectCategory.objects.get(subjectcategoryid = subject_category)
        else:
            subject_category = None

        current = Current.objects.get(subject=subject)
        current.category = category
        current.subjectcategory = subject_category
        current.processed = processed
        current.acquisition = acquisition
        current.note = note
        current.save()
        return HttpResponse(True)
    except Exception, e:
        print str(e)

def store_GAExport(request):
    """Accepts GA CSV export with unproccessed subjects""" 
    if request.FILES:
        return render_to_response("result.html", {"msg": upload.store_subjects_from_GAExport(request.FILES["file"]), })
    else:
        return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})
