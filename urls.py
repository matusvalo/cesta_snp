from django.conf.urls.defaults import *
from django.conf import settings
from paste_bin.views import URL_LEN

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
     (r'^pastebin/$', 'paste_bin.views.index'),
     (r'^pastebin/save/$', 'paste_bin.views.save'),
     (r'^pastebin/record/(?P<urlstr>.{{{0}}})$'.format(URL_LEN), 'paste_bin.views.viewrec'),
     (r'^pastebin/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
