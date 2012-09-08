#coding: utf-8
import os

from itertools import *

from django.db import connection
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings

from log_analysis.log.models import Current
from log_analysis.forms import EditForm, FilterForm

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

def data_edit(request):
    """Returns view on current data ordered by count"""
    #terms = Current.objects.filter(count__gt = 6).order_by("-count")
    # print request.GET
    edit_form = EditForm()
    filter_form = FilterForm()
    terms = query_to_dicts("""SELECT *  FROM log_current ORDER BY count DESC""")
    terms = list(terms)

    for i in xrange(len(terms)):
        terms[i]["subject"] = terms[i]["subject"].decode("utf8")
        terms[i]["note"] = terms[i]["note"].decode("utf8")

    page_interval = 150
    terms, filters = filter_data(terms, dict(request.GET), page_interval)
    next, previous = get_pagination(len(terms), page_interval, filters["page"])

    if next == "inactive":
        terms = terms[page_interval*filters["page"]:]
    else:
        terms = terms[page_interval*filters["page"]:page_interval*filters["page"]+page_interval]
    
    return render_to_response("data_edit.html", {'terms': terms, "edit_form": edit_form, "filter_form": filter_form, "filters":filters, "next": next, "previous":previous})

def filter_data(terms, filters, interval):
    for f in filters:
        if filters[f]:
            # if f == "term_search":
            #     terms = [t for t in terms if filters[f] in t["subject"]]

            # if f == "note":
            #     terms = [t for t in terms if filters[f] in t["note"]]

            if f == "filter_category" and filters[f][0] != "0":
                filters[f] = [int(num) for num in filters[f]]
                terms = [t for t in terms if t["category_id"] in [int(num) for num in filters[f]]]
                filters[f] = ";".join([str(num) for num in filters[f]])

            if f == "filter_subject_category" and filters[f][0] != "0":
                filters[f] = [int(num) for num in filters[f]]
                terms = [t for t in terms if t["subjectcategory_id"] in filters[f]]
                filters[f] = ";".join([str(num) for num in filters[f]])

            if f == "date_from":
                filters[f] = filters[f][0]
                if filters[f]:
                    month, year = int(filters[f].split("/")[0]), int(filters[f].split("/")[1])
                    terms = [t for t in terms if t["date"].month>=month and t["date"].year>=year]
            
            if f == "date_to":
                filters[f] = filters[f][0]
                if filters[f]:
                    month, year = int(filters[f].split("/")[0]), int(filters[f].split("/")[1])
                    terms = [t for t in terms if t["date"].month<=month and t["date"].year<=year]

            if f == "acquisition":
                filters[f] = "1"
                terms = [t for t in terms if t["acquisition"]]

            if f == "hide_processed":
                filters[f] = filters[f][0]
                terms = [t for t in terms if not t["processed"]]

    if "page" in filters.keys():
        filters["page"] = int(filters["page"][0])
    else:
        filters["page"] = 0

    return terms, filters

def get_pagination(count, interval, page):
    page_count = count/interval
    next = "active"
    previous = "active"

    if page == 0:
        previous = "inactive"
        if count <= interval:
            next = "inactive"
    else:
        previous = "active"
        if count <= interval*(page+1):
            next = "inactive"

    return next, previous