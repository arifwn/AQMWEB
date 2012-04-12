'''
Created on Sep 27, 2011

@author: Arif
'''

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def new_task(request):
    ''' View for WRF Task Creation '''
    from wrf.forms import NewTaskForm
    from wrf.models import Setting, Task
    
    if request.method == 'POST':
        task_form = NewTaskForm(request.POST)
        if task_form.is_valid():
            task_name = task_form.cleaned_data['task_name']
            task_description = task_form.cleaned_data['task_description']
            task_namelist_wps = task_form.cleaned_data['task_namelist_wps']
            task_namelist_wrf = task_form.cleaned_data['task_namelist_wrf']
            task_namelist_arwpost = task_form.cleaned_data['task_namelist_arwpost']
            
            # TODO: handle ChemData setting
            
            wrf_setting = Setting(name=task_name, user=request.user,
                                  description=task_description,
                                  namelist_wps=task_namelist_wps,
                                  namelist_wrf=task_namelist_wrf,
                                  namelist_arwpost=task_namelist_arwpost)
            
            wrf_setting.save()
            
            wrf_task = Task(name=task_name, user=request.user,
                                  description=task_description,
                                  setting=wrf_setting)
            wrf_task.save()
            
            messages.success(request, 'Task created successfully!')
            
            return(redirect('wrf_list_task'))
    else:
        task_form = NewTaskForm()
        
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request,
                                   {'form': task_form}))
    return HttpResponse(html)

@login_required
def list_task(request):
    from wrf.models import Task
    
    t = get_template('aqm_web/wrf/task-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def view_task(request, task_id):
    from wrf.models import Task
    
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404
    
    t = get_template('aqm_web/wrf/task-detail.html')
    html = t.render(RequestContext(request, {'task': task}))
    return HttpResponse(html)

# -- Task Group --
@login_required
def new_task_group(request):
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def list_task_group(request):
    t = get_template('aqm_web/wrf/task-group-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def task_group_detail(request):
    t = get_template('aqm_web/wrf/task-group-detail.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

# -- Chem Data Views --
@login_required
def new_chem_data(request):
    '''view to create a new ChemData'''
    from aqm_web.forms import ChemDataForm
    from aqm_web.misc import sanitize_html
    from wrf.models import ChemData
    
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
            
            chemdata = ChemData(name=name, description=sanitize_html(description), data=data_file, user=request.user)
            chemdata.save()
            
            return redirect('wrf_new_chem_data_step2', chemdata.pk)
        else:
            logger.debug('not valid')
    else:
        form = ChemDataForm()
    
    t = get_template('aqm_web/wrf/new-chem-data.html')
    html = t.render(RequestContext(request, {
                                             'form': form
                                             }))
    return HttpResponse(html)

@login_required
def new_chem_data_step2(request, id):
    '''step 2 in ChemData creation'''
    import os.path
    from wrf.models import ChemData
    
    try:
        chemdata = ChemData.objects.get(pk=id)
    except ChemData.DoesNotExist:
        raise Http404
    
    t = get_template('aqm_web/wrf/new-chem-data2.html')
    html = t.render(RequestContext(request, {
                                             'chemdata': chemdata,
                                             'filename': os.path.basename(chemdata.data.name)
                                             }))
    return HttpResponse(html)

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
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def remove_chem_data(request):
    '''view to remove a new chem data'''
    t = get_template('aqm_web/wrf/new-task.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def list_chem_data(request):
    '''list available chem data'''
    t = get_template('aqm_web/wrf/chem-data-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def popup_new_task_chem_data(request):
    '''TODO: this dummy view is accessed from create task page 
    as a popup. replace it'''
    t = get_template('aqm_web/wrf/popup-chem-select-data.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)


@login_required
def list_meteo_data(request):
    t = get_template('aqm_web/wrf/meteo-data-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

@login_required
def list_model_setting(request):
    t = get_template('aqm_web/wrf/model-setting-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)
