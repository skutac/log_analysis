#coding: utf-8
import os, datetime, csv, re

from itertools import *

from django.db import connection
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

from log_analysis.psh_db.models import Hesla, Ekvivalence, Varianta
from log_analysis.log.models import Current, Category, SubjectCategory, SubjectCount

def query_to_dicts(query_string, *query_args):
    """Run a simple query and produce a generator
    that returns the results as a bunch of dictionaries
    with keys for the column values selected.
    """
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        yield row_dict
    return

hesla = query_to_dicts("""SELECT heslo FROM psh_db.hesla""")
hesla = set([h["heslo"].encode("utf8") for h in hesla])

ekvivalence = query_to_dicts("""SELECT ekvivalent FROM psh_db.ekvivalence""")
ekvivalence = set([h["ekvivalent"].encode("utf8") for h in ekvivalence])

varianta = query_to_dicts("""SELECT varianta FROM psh_db.varianta""")
varianta = set([h["varianta"].encode("utf8") for h in varianta])

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
        return render_to_response("result.html", {"msg": store_subjects_from_GAExport(request.FILES["file"]), })
    else:
        return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})

def save_to_current(term, count):
    """Updates database with current subject:count pair. Creates it if not already there."""
    attrs = {"subject":term, "count":count}
    if term in hesla or term in ekvivalence:
        attrs["category"] = Category.objects.get(categoryid=4)
        attrs["subjectcategory"] = SubjectCategory.objects.get(subjectcategoryid=11)
        attrs["processed"] = 1
    elif term in varianta:
        attrs["category"] = Category.objects.get(categoryid=4)
        attrs["subjectcategory"] = SubjectCategory.objects.get(subjectcategoryid=12)
        attrs["processed"] = 1
    
    try:
        obj = Current.objects.get(subject=term)
        obj.count += int(count)
    except Exception:
        obj = Current(**attrs)

    obj.save()

    obj_count = SubjectCount(subject=obj, count=attrs["count"])
    obj_count.save()
    return

def store_subjects_from_GAExport(export):
    """Stores subjects from GA CSV export."""
    old_count = Current.objects.count()
    switch = False
    old = "**********"
    for line in export.readlines():
        if switch:
            try:
                items = re.search("(.*?),(\d+),", line)
                term, count = items.group(1).strip("\""), items.group(2)
            except Exception, e:
                pass

            term = term.strip(" ")
            if term != "":
                if term == old:
                    switch = False
                else:
                    save_to_current(term, count)
                    old = term

        elif "Vyhledávací dotaz," in line or "Search Term," in line:
            switch = True

    export.close()

    total_count = Current.objects.count()
    new_count = total_count - old_count
    return u"Nově nahráno: %s (%s celkem)" %(new_count, total_count)
