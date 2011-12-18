'''
Created on Sep 18, 2011

@author: Arif
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'aqm_web.views.generic.index', name='index'),
    url(r'^status/$', 'aqm_web.views.generic.status', name='status'),
    url(r'^wrf/new/$', 'aqm_web.views.wrf.new_task', name='wrf_new_task'),
    url(r'^wrf/new-group/$', 'aqm_web.views.wrf.new_task_group', name='wrf_new_task_group'),
    url(r'^wrf/new/popup-chem-data$', 'aqm_web.views.wrf.popup_new_task_chem_data', name='wrf_popup_new_task_chem_data'),
    
    url(r'^wrf/task-list/$', 'aqm_web.views.wrf.task_list', name='wrf_task_list'),
    url(r'^wrf/task-group-list/$', 'aqm_web.views.wrf.task_group_list', name='wrf_task_group_list'),
    url(r'^wrf/task-group-details/$', 'aqm_web.views.wrf.task_group_details', name='wrf_task_group_details'),
    url(r'^wrf/chem-data-list/$', 'aqm_web.views.wrf.chem_data_list', name='wrf_chem_data_list'),
    url(r'^wrf/meteo-data-list/$', 'aqm_web.views.wrf.meteo_data_list', name='wrf_meteo_data_list'),
    url(r'^wrf/model-setting-list/$', 'aqm_web.views.wrf.model_setting_list', name='wrf_model_setting_list'),
    
    (r'^plot/mercator$', 'aqm_web.views.plot.mercator'),
    (r'^plot/lambert-conformal$', 'aqm_web.views.plot.lambert_conformal'),
    
    (r'^testview/$', 'aqm_web.views.generic.testview'),
    (r'^testview-popup/$', 'aqm_web.views.generic.testview_popup'),
    (r'^plot/test$', 'aqm_web.views.plot.test_plot'),
    
    # Remove this in production
#    (r'^static/aqm_web/(.*)$', 'aqm_web.views.debug_static'),
    
    url(r'^web_api/get_namelist.([-\w]+)$', 'aqm_web.views.web_api.get_namelist', name='api_get_namelist'),
    
    # handle user login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/change_password/$', 'django.contrib.auth.views.password_change'),
    url(r'^accounts/change_password_done/$', 'django.contrib.auth.views.password_change_done'),
    
    #for testing purpose
    (r'^plotview/$', 'aqm_web.views.generic.plotview'),
)