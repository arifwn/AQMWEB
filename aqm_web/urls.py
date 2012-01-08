'''
Created on Sep 18, 2011

@author: Arif
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('aqm_web.views.generic',
    url(r'^$', 'index', name='index'),
    url(r'^status/$', 'status', name='status'),
    
    (r'^testview/$', 'testview'),
    (r'^testview-popup/$', 'testview_popup'),
    
    #for testing purpose
    (r'^plotview/$', 'plotview'),
)

urlpatterns += patterns('aqm_web.views.wrf',
    url(r'^wrf/new/$', 'new_task', name='wrf_new_task'),
    url(r'^wrf/list-task/$', 'list_task', name='wrf_list_task'),
    
    url(r'^wrf/new-group/$', 'new_task_group', name='wrf_new_task_group'),
    url(r'^wrf/task-group-details/$', 'task_group_details', name='wrf_task_group_details'),
    url(r'^wrf/list-task-group/$', 'list_task_group', name='wrf_list_task_group'),
    
    url(r'^wrf/new-chem-data/$', 'new_chem_data', name='wrf_new_chem_data'),
    url(r'^wrf/new/popup-chem-data$', 'popup_new_task_chem_data', name='wrf_popup_new_task_chem_data'),
    url(r'^wrf/list-chem-data/$', 'list_chem_data', name='wrf_list_chem_data'),
    
    url(r'^wrf/list-meteo-data/$', 'list_meteo_data', name='wrf_list_meteo_data'),
    url(r'^wrf/list-model-setting/$', 'list_model_setting', name='wrf_list_model_setting'),
)

urlpatterns += patterns('aqm_web.views.plot',
    (r'^plot/mercator$', 'mercator'),
    (r'^plot/lambert-conformal$', 'lambert_conformal'),
    (r'^plot/test$', 'test_plot'),
)
