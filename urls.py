from django.conf.urls.defaults import *
from django.conf import settings
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^log_analysis/', include('log_analysis.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^log_analysis/admin/', include(admin.site.urls)),

    (r'^log_analysis/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.ROOT, 'static').replace('\\','/')}),
    (r'^log_analysis/$', 'views.redirect'),
    (r'^log_analysis/index$', 'views.index'),
    (r'^log_analysis/store_GAExport$', 'handler.store_GAExport'),
    (r'^log_analysis/data_edit$', 'views.data_edit'),
    (r'^log_analysis/graph_export$', 'views.data_edit'),
    (r'^log_analysis/export_graph_as_png$', 'views.export_graph_as_png'),
    (r'^log_analysis/store_updated_row$', 'handler.store_updated_row'),
    (r'^log_analysis/login$', 'views.login'),
    (r'^log_analysis/user_login$', 'user_handler.login_user'),
    (r'^log_analysis/user_logout$', 'user_handler.logout_user'),
    # (r'^.*$', 'views.index'),
)
