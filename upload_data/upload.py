#coding: utf-8
import re, datetime, os, csv

from log_analysis.log.models import Old, Current, Terms
from log_analysis.psh_db.models import Hesla, Ekvivalence, Varianta

from django.conf import settings
from django.utils.encoding import smart_str, smart_unicode

def storeSubjectsFromCSV(csvfile):
    """Stores proccessed subjects from CSV file to database"""
    lines = csv.reader(csvfile, delimiter=",", quotechar='"')

    oldCount = Old.objects.count()
    for line in lines:
        current = line[3]
        obj, created = Old.objects.get_or_create(subject=current)
        if created:
            obj.save()
        try:
            obj = Current.objects.get(subject=current)
            obj.delete()
        except Exception, e:
            #return str(e)
            continue
    totalCount = Old.objects.count()
    newCount = totalCount - oldCount
    return u"Do zpracovaných hesel přibylo: %s (%s celkem)" %(newCount, totalCount)

def makeTermStatistic(lines, subrange_left, subrange_right, regexp):
    """Analyzes the text file according to given parameters and returns the term:count statistics in the form of CS file."""
    blank = Terms.objects.all().delete()
    terms = []

    if not regexp:
        if subrange_left:
            subrange_left = int(subrange_left)
        else:
            subrange_left = 0
        if subrange_right:
            subrange_right = int(subrange_right)

        for line in lines:
            term = line[subrange_left:subrange_right].strip("\n|\r|\r\n").lower()
            terms.append(term)
    else:
        terms = re.findall(regexp, lines.read(), re.IGNORECASE)
        terms = [term.strip("\n|\r|\r\n").lower() for term in terms]

    for term in terms:
        try:
            obj = Terms.objects.get(term=term)
            obj.count += 1
            obj.save()
        except:
            obj = Terms(term=term, count=1)
            obj.save()

    count = Terms.objects.count()

    output = open(os.path.join(settings.ROOT, "static/logy_csv/", lines.name), "w")
    output.write("termín, počet\n")
    for term in Terms.objects.all().order_by("count").reverse():
        output.write("".join([term.term.encode("utf8"), ",", str(term.count), "\n"]))
    output.close()

    return " ".join([u"Počet termínů:", str(count), u"<div>Soubor ke stažení: <a href='static/logy_csv/%s'>%s</a></div>"%(lines.name, lines.name)])

def makeCSV():
    """Create the HttpResponse object with the appropriate CSV header."""
    filename = "logy-%s.csv" %datetime.date.today()
    csv = open(os.path.join(settings.ROOT, "static/logy_csv/", filename), "w")

    csv.write("'datum vytvoření hesla', 'počet', 'zkratka', 'termín', 'N/D', 'kontrol. č.', 'pozn.'\n")
    objects = Current.objects.order_by("count").reverse()
    for obj in objects:
        csv.write(", %s, , %s, , , \n" %(obj.count, obj.subject.encode("utf8")))

    csv.close()	
    return filename

def saveToCurrent(term, count):
    """Updates database with current subject:count pair. Creates it if not already there."""
    old = Old.objects.filter(subject=term)
    hesla = Hesla.objects.using('psh_db').filter(heslo=term)
    ekvivalence = Ekvivalence.objects.using('psh_db').filter(ekvivalent=term)
    varianta = Varianta.objects.using('psh_db').filter(varianta=term)
    test = len(old) + len(hesla) + len(ekvivalence) + len(varianta)
    if test == 0:
        try:
            obj = Current.objects.get(subject=term)
            obj.count = obj.count + int(count)
            obj.save()
        except:
            obj = Current(subject=term, count=int(count))
            obj.save()



def storeSubjectsFromGAExport(export):
    """Stores subjects from GA CSV export."""
    old_count = Current.objects.count()
    #i = 0
    switch = False

    for line in export.readlines():
        #if line.startswith("# -----"):
                #switch = False

        if switch:
            try:
                items = re.search("(.*?),(\d+),", line)
                #items = re.search("(.*?),(\d+),\d+", line)
                term, count = items.group(1).strip("\""), items.group(2)
            except Exception, e:
                pass

            term = term.strip(" ")
            if term != "":
                saveToCurrent(term, count)

        elif "Vyhledávací dotaz" in line:
            switch = True

    export.close()

    total_count = Current.objects.count()
    new_count = total_count - old_count
    return u"Nově nahráno: %s (%s celkem)" %(new_count, total_count)