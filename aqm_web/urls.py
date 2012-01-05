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
    url(r'^wrf/new-group/$', 'new_task_group', name='wrf_new_task_group'),
    url(r'^wrf/new/popup-chem-data$', 'popup_new_task_chem_data', name='wrf_popup_new_task_chem_data'),
    
    url(r'^wrf/task-list/$', 'task_list', name='wrf_task_list'),
    url(r'^wrf/task-group-list/$', 'task_group_list', name='wrf_task_group_list'),
    url(r'^wrf/task-group-details/$', 'task_group_details', name='wrf_task_group_details'),
    url(r'^wrf/chem-data-list/$', 'chem_data_list', name='wrf_chem_data_list'),
    url(r'^wrf/meteo-data-list/$', 'meteo_data_list', name='wrf_meteo_data_list'),
    url(r'^wrf/model-setting-list/$', 'model_setting_list', name='wrf_model_setting_list'),
)

urlpatterns += patterns('aqm_web.views.plot',
    (r'^plot/mercator$', 'mercator'),
    (r'^plot/lambert-conformal$', 'lambert_conformal'),
    (r'^plot/test$', 'test_plot'),
)
