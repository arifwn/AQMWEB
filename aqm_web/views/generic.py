from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
import os
import django.views.static

def debug_static(request, path):
    parent = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(parent, 'static', 'aqm_web')
    return django.views.static.serve(request, path, root)

@login_required
def index(request):
    t = get_template('aqm_web/status.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def status(request):
    t = get_template('aqm_web/status.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)
    

@login_required
def plotview(request):
    t = get_template('aqm_web/plotview.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

def testview(request):
    t = get_template('aqm_web/test.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

def testview_popup(request):
    t = get_template('aqm_web/test_popup.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)
