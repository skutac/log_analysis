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
    (r'^$', 'views.redirect'),
    (r'^index$', 'views.index'),
    (r'^store_GAExport$', 'handler.store_GAExport'),
    (r'^data_edit$', 'views.data_edit'),
    (r'^graph_export$', 'views.data_edit'),
    (r'^export_graph_as_png$', 'views.export_graph_as_png'),
    (r'^store_updated_row$', 'handler.store_updated_row'),
    (r'^acquisition_export$', 'views.get_acquisition_export'),
    (r'^login$', 'views.user_login'),
    (r'^.*$', 'views.index'),
)
