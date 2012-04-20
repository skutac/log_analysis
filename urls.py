from django.conf.urls.defaults import *
from django.conf import settings
import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^log_analysis/', include('log_analysis.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.ROOT, 'static').replace('\\','/')}),
    (r'^$', 'views.index'),
    (r'^index$', 'views.index'),
    (r'^storeCSV$', 'handler.storeCSV'),
    (r'^storeGAExport$', 'handler.storeGAExport'),
    (r'^extractSubjects$', 'handler.extractSubjects'),
    #(r'^deleteArchive$', 'handler.deleteArchive'),
    (r'^termStatistic$', 'handler.termStatistic'),
    (r'^export_data$', 'handler.export_data'),
    (r'^data_view$', 'views.data_view'),
    (r'^.*$', 'views.index'),
)
