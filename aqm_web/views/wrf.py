'''
Created on Sep 27, 2011

@author: Arif
'''
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse

@login_required
def new_task(request):
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def new_task_group(request):
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def popup_new_task_chem_data(request):
    t = get_template('aqm_web/wrf/popup-chem-select-data.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def task_list(request):
    t = get_template('aqm_web/wrf/task-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def task_group_list(request):
    t = get_template('aqm_web/wrf/task-group-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def task_group_details(request):
    t = get_template('aqm_web/wrf/task-group-details.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def chem_data_list(request):
    t = get_template('aqm_web/wrf/chem-data-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def meteo_data_list(request):
    t = get_template('aqm_web/wrf/meteo-data-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def model_setting_list(request):
    t = get_template('aqm_web/wrf/model-setting-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)
