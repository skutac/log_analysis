#coding: utf-8
import os, json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings

from log_analysis.log.models import Current, Category, SubjectCategory
from log_analysis.forms import EditForm, FilterForm
from log_analysis.handler import query_to_dicts


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

def get_acquisition_export(request):
    pass

def data_edit(request):
    """Returns view on current data ordered by count"""
    #terms = Current.objects.filter(count__gt = 6).order_by("-count")
    print request.GET
    edit_form = EditForm()
    filter_form = FilterForm()
    terms = query_to_dicts("""SELECT *  FROM log_current ORDER BY count DESC""")
    terms = list(terms)

    for i in xrange(len(terms)):
        terms[i]["subject"] = terms[i]["subject"].decode("utf8")
        terms[i]["note"] = terms[i]["note"].decode("utf8")

    page_interval = 150
    terms, filters = filter_data(terms, dict(request.GET), page_interval)
    next, previous, page_count = get_pagination(len(terms), page_interval, filters["page"])

    graph_data = False
    if "graph" in filters.keys():
        graph_data = get_graph_data(terms, filters)


    if next == "inactive":
        terms = terms[page_interval*filters["page"]:]
    else:
        terms = terms[page_interval*filters["page"]:page_interval*filters["page"]+page_interval]

    return render_to_response("data_edit.html", {'terms': terms, "edit_form": edit_form, "filter_form": filter_form, "filters":filters, "next": next, "previous":previous, "page_count":page_count, "graph_data": graph_data})

def filter_data(terms, filters, interval):
    no_subject_category = True
    only_subject = False
    for f in filters:
        if filters[f]:
            if f == "term_search":
                filters[f] = filters[f][0]
                terms = [t for t in terms if filters[f] in t["subject"]]

            # if f == "note":
            #     terms = [t for t in terms if filters[f] in t["note"]]

            if f == "filter_category" and filters[f][0] != "0":
                filters[f] = [int(num) for num in filters[f]]
                category_ids = [int(num) for num in filters[f]]
                terms = [t for t in terms if t["category_id"] in category_ids]
                filters[f] = ";".join([str(num) for num in filters[f]])

                if len(category_ids) == 1 and category_ids[0] == 4:
                    only_subject = True
                else:
                    only_subject = False

            elif f == "filter_subject_category" and filters[f][0] != "0":
                filters[f] = [int(num) for num in filters[f]]
                terms = [t for t in terms if t["subjectcategory_id"] in filters[f]]
                filters[f] = ";".join([str(num) for num in filters[f]])
                no_subject_category = False


            elif f == "date_from":
                filters[f] = filters[f][0]
                if filters[f]:
                    month, year = int(filters[f].split("/")[0]), int(filters[f].split("/")[1])
                    terms = [t for t in terms if t["date"].month>=month and t["date"].year>=year]
            
            elif f == "date_to":
                filters[f] = filters[f][0]
                if filters[f]:
                    month, year = int(filters[f].split("/")[0]), int(filters[f].split("/")[1])
                    terms = [t for t in terms if t["date"].month<=month and t["date"].year<=year]

            elif f == "acquisition":
                filters[f] = "1"
                terms = [t for t in terms if t["acquisition"]]

            elif f == "hide_processed":
                filters[f] = filters[f][0]
                terms = [t for t in terms if not t["processed"]]

            elif f == "graph":
                filters[f] = int(filters[f][0])

    if no_subject_category and only_subject:
        terms = [t for t in terms if not(t["subjectcategory_id"])]

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

    return next, previous, page_count+1

def get_graph_data(terms, filters):
    graph_data = {}
    graph_id = filters["graph"]
    terms = [t for t in terms if t["processed"]]

    if graph_id == 1:
        key = "category_id"
        keys = set([t[key] for t in terms])
        categories = list(query_to_dicts("""SELECT * FROM log_category"""))

        keys2label = {}
        for c in categories:
            keys2label[c["categoryid"]] = c["category"]

    elif graph_id == 2:
        terms = [t for t in terms if t["category_id"] == 4]
        key = "subjectcategory_id"
        keys = set([t[key] for t in terms])
        subject_categories = list(query_to_dicts("""SELECT * FROM log_subjectcategory"""))
        keys2label = {}

        for c in subject_categories:
            keys2label[c["subjectcategoryid"]] = c["subjectcategory"]

    elif graph_id == 3:
        terms = [t for t in terms if t["category_id"] == 1]
        key = "acquisition"
        keys = set([t[key] for t in terms])
        keys2label = {0:"fond", 1:"akvizice"}

    else:
        return False

    data = {}
    
    for k in keys:
        if k != None:
            data[keys2label[k]] = 0

    for t in terms:
        if t[key] != None:
            data[keys2label[t[key]]] += 1

    data = [[d, data[d]] for d in data.keys()]
    data.insert(0, ["", 0])

    graph_data["data"] = data

    date = list(query_to_dicts("""SELECT date FROM log_current ORDER BY date"""))

    if not filters["date_to"]:
        graph_data["date_to"] = "/".join([str(date[-1]["date"].month), str(date[-1]["date"].year)])
    else:
        graph_data["date_to"] = filters["date_to"]

    if not filters["date_from"]:
        graph_data["date_from"] = "/".join([str(date[0]["date"].month), str(date[0]["date"].year)])
    else:
        graph_data["date_from"] = filters["date_from"]

    graph_data["count"] = len(terms)

    return graph_data

def export_graph_as_png(request):
    graph = request.POST["graph"].split(",")[-1]
    graph = graph.decode("base64")
    response = HttpResponse(graph, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="graph.png"'
    return response