#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from upload_data import upload
from django.conf import settings
from log_analysis.log.models import Current
import os, datetime, csv

def storeCSV(request):
  """Accepts CSV file with proccessed subjects""" 
  if request.FILES:
    return render_to_response("result.html", {"msg": upload.storeSubjectsFromCSV(request.FILES["file"]), })
  else:
    return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})

def storeGAExport(request):
  """Accepts GA CSV export with unproccessed subjects""" 
  if request.FILES:
    return render_to_response("result.html", {"msg": upload.storeSubjectsFromGAExport(request.FILES["file"]), })
  else:
    return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})
        
def termStatistic(request):
    """Initiates proccess of analyzing text file according to set parameters"""
    if request.FILES:
        #if request.POST["subrange_left"]:
        try:
            subrange_left = int(request.POST["subrange_left"])
        except Exception, e:
            subrange_left = 0
            
        #if request.POST["subrange_right"]:
        try:
            subrange_right = (int(request.POST["subrange_right"])+1)*(-1)
        except Exception, e:
            subrange_right = None
            
	return render_to_response("result.html", {"msg": upload.makeTermStatistic(request.FILES["file"], subrange_left, subrange_right, request.POST["regexp"])})
    else:
	return render_to_response("error.html", {'error': 'Nebyl vybrán žádný soubor.'})

def export_data(request):
    """Creates the HttpResponse object with the appropriate CSV header."""
    filename = "logy-export-%s.csv" %datetime.date.today()
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = "".join(['attachment; filename=', filename])
    objects = Current.objects.filter(count__gt=3).order_by("-count")
    objects_gt_2 = Current.objects.filter(count__gt=2).order_by("-count")
    
    if len(objects) < 200:
        objects = objects_gt_2
    
    writer = csv.writer(response)
    writer.writerow(['datum vytvoření hesla', 
    'počet', 
    'zkratka', 
    'termín', 
    'N/D', 
    'kontrol. č.', 
    'pozn.'])

    for obj in objects:
	writer.writerow(["", obj.count, "", obj.subject.encode("utf8"), "", "", ""])
    return response
    
#def deleteArchive(request):
    #try:
        #archive = request.POST['archive']
        #os.system("rm %s" %(os.path.join(settings.ROOT, "static/logy_csv", archive)))
        #return HttpResponse('ok')
    #except Exception, e:
        #return HttpResponse(str(e))
        

#def extractSubjects(request):
        #try:
	   #for log in os.listdir(os.path.join(settings.ROOT, "static/logy")):
	       ##if "test" in log:
	           #path = os.path.join(settings.ROOT, "static/logy", log)
                   #upload.extractSubjectsFromLog(path)
		   ##os.system("rm %s" %path)

		   #csv = upload.makeCSV()
		   #responseDict = {"count" : Current.objects.count(), "csv" : csv, "csvURL": "static/logy_csv/" + csv,}
		   #response = u"<div id='csv'>CSV soubor ke stažení: <a href='%s'>%s</a></div><div>Celkový počet termínů: %s</div><div><a href='index'>Zpět na hlavní stránku -&gt;</a></div>"
	   #return HttpResponse(response%(responseDict["csvURL"], responseDict["csv"], responseDict["count"], ))
	#except Exception, e:
	   #return HttpResponse(e)