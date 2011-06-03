import datetime
import re
from models import record
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db import IntegrityError
from urlgenerator import RandomUrl
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
URL_LEN = 5
URL_GEN_TRIES = 10

def index(request):
    return render_to_response("paste_bin/index.html", context_instance = RequestContext(request))

def save(request):
    match = re.match(r'(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})', request.POST["date"])
    groups = match.groupdict()
    edate = datetime.date(int(groups['year']), int(groups['month']), int(groups['day']))

    rec = None
    try:
        for rand_url in RandomUrl(URL_LEN, URL_GEN_TRIES):
            rec = record(url = rand_url, name = request.POST["name"], title = request.POST["title"],
                         text = request.POST["text"], exp_date = edate)
            try:
                rec.save(force_insert = True)
                break
            except IntegrityError:
                pass
    except LookupError:
        return HttpResponse("<b>Cannot search new URL</b>")

    return HttpResponseRedirect(reverse('paste_bin.views.viewrec', args = (rec.url,)))

def search(request):
    query = request.GET.get('q', '')
    namerecs = record.objects.filter(name = query)
    titlerecs = record.objects.filter(title = query)
    has_namerecs = True if len(namerecs) != 0 else False
    has_titlerecs = True if len(titlerecs) != 0 else False
    return render_to_response('paste_bin/search.html',
                              {'namerecs':namerecs,
                               'titlerecs':titlerecs,
                               'found_name':has_namerecs,
                               'found_title':has_titlerecs
                              }
                             )

def viewrec(request, urlstr):
    record.rem_old_records()                        #removing old records
    try:
        rec = record.objects.get(url = urlstr)
    except ObjectDoesNotExist:
        return HttpResponse("<b>Record doesn't exist.</b>")
    url = reverse('paste_bin.views.viewrec', args = (rec.url,))
    return render_to_response('paste_bin/viewrec.html',
                              {'title':rec.title,
                               'name':rec.name,
                               'text':rec.text,
                               'exp_date':rec.exp_date.date(),
                               'url':url
                              }
                             )

