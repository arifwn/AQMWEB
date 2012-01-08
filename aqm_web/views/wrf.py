'''
Created on Sep 27, 2011

@author: Arif
'''
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import redirect

import logging

logger = logging.getLogger(__name__)

@login_required
def new_task(request):
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def list_task(request):
    t = get_template('aqm_web/wrf/task-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)


# -- Task Group --
@login_required
def new_task_group(request):
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def list_task_group(request):
    t = get_template('aqm_web/wrf/task-group-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def task_group_details(request):
    t = get_template('aqm_web/wrf/task-group-details.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

# -- Chem Data Views --
@login_required
def new_chem_data(request):
    '''view to create a new ChemData'''
    from aqm_web.forms import ChemDataForm
    
    if request.method == 'POST':
        form = ChemDataForm(request.POST, request.FILES)
        if form.is_valid(): 
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            parameters_json = form.cleaned_data['parameters_json']
            
            data_file = form.cleaned_data['data']
            
            logger.debug('name: %s' % name)
            logger.debug('description: %s' % description)
            logger.debug('parameters_json: %s' % parameters_json)
            logger.debug('data_file: %s' % data_file)
#            return redirect('view-profile', request.user.username)
        else:
            logger.debug('not valid')
    else:
        form = ChemDataForm()
    
    t = get_template('aqm_web/wrf/new-chem-data.html')
    html = t.render(RequestContext(request, {
                                             'section': 'wrf', 
                                             'form': form
                                             }))
    return HttpResponse(html)

@login_required
def new_chem_data_step2(request):
    '''step 2 in ChemData creation'''

@login_required
def new_pollutant_params_popup(request):
    '''to be used from ChemData create/edit view'''

@login_required
def edit_pollutant_params_popup(request):
    '''to be used from ChemData create/edit view'''

@login_required
def remove_pollutant_params_popup(request):
    '''to be used from ChemData create/edit view'''


    

@login_required
def modify_chem_data(request):
    '''view to modify a new chem data'''
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def remove_chem_data(request):
    '''view to remove a new chem data'''
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def list_chem_data(request):
    '''list available chem data'''
    t = get_template('aqm_web/wrf/chem-data-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def popup_new_task_chem_data(request):
    '''TODO: this dummy view is accessed from create task page 
    as a popup. replace it'''
    t = get_template('aqm_web/wrf/popup-chem-select-data.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)


@login_required
def list_meteo_data(request):
    t = get_template('aqm_web/wrf/meteo-data-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)

@login_required
def list_model_setting(request):
    t = get_template('aqm_web/wrf/model-setting-list.html')
    html = t.render(RequestContext(request, {'section': 'wrf'}))
    return HttpResponse(html)
