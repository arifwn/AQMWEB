
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages

from aqm_utils.sanitizer import sanitize_html


@login_required
def new_task(request):
    '''View for AERMOD Task Creation.'''
    from aermod.forms import NewTaskForm
    from aermod.models import Setting, Task
    from wrf.models import Task as WRFTask
    
    if request.method == 'POST':
        task_form = NewTaskForm(request.POST)
        if task_form.is_valid():
            task_name = task_form.cleaned_data['task_name']
            task_description = sanitize_html(task_form.cleaned_data['task_description'])
            hillheight_setting = task_form.cleaned_data['hillheight_setting']
            meteorology_setting = task_form.cleaned_data['meteorology_setting']
            aermod_setting = task_form.cleaned_data['aermod_setting']
            plot_setting = task_form.cleaned_data['plot_setting']
            wrf_task = task_form.cleaned_data['wrf_task']
            
            aermod_setting = Setting(user=request.user,
                                     hillheight_setting=hillheight_setting,
                                     meteorology_setting=meteorology_setting,
                                     aermod_setting=aermod_setting,
                                     plot_setting=plot_setting)
            aermod_setting.save()
            
            aermod_task = Task(name=task_name,
                               user=request.user,
                               description=task_description,
                               setting=aermod_setting)
            aermod_task.save()
            
            messages.success(request, 'Task created successfully!')
            
            return(redirect('aermod-task-list'))
    else:
        task_form = NewTaskForm()
        
    t = get_template('aqm_web/aermod/new-task.html')
    html = t.render(RequestContext(request,
                                   {'form': task_form}))
    return HttpResponse(html)


@login_required
def list_task(request):
    '''List all available task.'''
    t = get_template('aqm_web/aermod/task-list.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)


@login_required
def view_task(request, task_id):
    '''Display task details.'''
    t = get_template('aqm_web/aermod/task-detail.html')
    html = t.render(RequestContext(request, {}))
    return HttpResponse(html)

