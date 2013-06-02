#coding: utf-8
import os, datetime, csv, re

from itertools import *

from django.db import connection
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required

from log_analysis.log.models import Category, SubjectCategory, SubjectCount, Subjects

import user_handler

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

        subject = Subjects.objects.get(subject=subject)
        subject.category = category
        subject.subjectcategory = subject_category
        subject.processed = processed
        subject.acquisition = acquisition
        subject.note = note
        subject.save()
        return HttpResponse(True)
    except Exception, e:
        print str(e)

@login_required
def store_GAExport(request):
    """Store GA CSV export""" 
    username = request.user
    if request.FILES:
        return render_to_response("result.html", {"msg": store_subjects_from_GAExport(request.FILES["file_field"], username=username), })
    else:
        return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})

def save_subject(term, count, date, user):
    """Updates database with current subject:count pair. Creates it if not already there."""
    subject = {"subject":term, "date": date}
    if term in hesla or term in ekvivalence:
        subject["category"] = Category.objects.get(categoryid=4)
        subject["subjectcategory"] = SubjectCategory.objects.get(subjectcategoryid=11)

    elif term in varianta:
        subject["category"] = Category.objects.get(categoryid=4)
        subject["subjectcategory"] = SubjectCategory.objects.get(subjectcategoryid=12)

    obj, created = Subjects.objects.get_or_create(subject=term)    

    if created:
        if "category" in subject:
            obj.category = subject["category"]
            obj.subjectcategory = subject["subjectcategory"]
            obj.processed = 1

        obj.save()

    obj_count = SubjectCount(subject=obj, count=count, date=date, user=user)
    obj_count.save()
    return

def store_subjects_from_GAExport(export, username):
    """Stores subjects from GA CSV export."""
    old_count = Subjects.objects.count()
    switch = False
    dates = []
    terms = []
    old = "**********"
    user = user_handler.get_user(username)

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
                    terms.append((term, count))
                    old = term

        elif "Vyhledávací dotaz," in line or "Search Term," in line:
            switch = True

        line_split = line.split(",")
        if len(line_split) == 2 and re.match("\d+.\d+.\d+", line_split[0]):
            dates.append(line_split[0])

    export.close()

    date_delimiter = "."
    day_index = 0
    month_index = 1
    year_index = 2

    if "/" in dates[0]:
        date_delimiter = "/"
        day_index = 1
        month_index = 0
        year_index = 2
    
    dates = list(set([date_delimiter.join([d.split(date_delimiter)[month_index], d.split(date_delimiter)[year_index]]) for d in dates]))

    if len(dates) == 1:
        date_split = dates[0].split(date_delimiter)
        year = "".join(["20", date_split[1]])
        date = "-".join([year, date_split[0], "01"])
    else:
        return "Chyba: Export obsahuje termíny z více než jednoho měsíce."

    for term in terms:
        if int(term[1]) > 0:
            save_subject(term[0], term[1], date, user)

    total_count = Subjects.objects.count()
    new_count = total_count - old_count
    return u"Nově nahráno: %s (%s celkem)" %(new_count, total_count)