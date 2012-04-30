'''
Created on Sep 18, 2011

@author: Arif
'''
from django.conf.urls.defaults import *
from piston.resource import Resource

from aqm_web import handlers_wrf

from aqm_web.authentication import CookieAuthentication

urlpatterns = patterns('aqm_web.views.generic',
    url(r'^$', 'index', name='index'),
    url(r'^status/$', 'status', name='status'),
    
    (r'^testview/$', 'testview'),
    (r'^testview-popup/$', 'testview_popup'),
    
    #for testing purpose
    (r'^plotview/$', 'plotview'),
)

urlpatterns += patterns('aqm_web.views.wrf_view',
    url(r'^wrf/new/$', 'new_task', name='wrf_new_task'),
    url(r'^wrf/task/(\d+)/$', 'view_task', name='wrf-task-detail'),
    url(r'^wrf/task/$', 'list_task', name='wrf-task-list'),
    
    url(r'^wrf/new-group/$', 'new_task_group', name='wrf_new_task_group'),
    url(r'^wrf/task-group-details/$', 'task_group_detail', name='wrf_task_group_detail'),
    url(r'^wrf/list-task-group/$', 'list_task_group', name='wrf_list_task_group'),
    
    url(r'^wrf/new-chem-data/$', 'new_chem_data', name='wrf_new_chem_data'),
    url(r'^wrf/new-chem-data-step2/(\d+)$', 'new_chem_data_step2', name='wrf_new_chem_data_step2'),
    url(r'^wrf/edit-chem-data/(\d+)$', 'edit_chem_data', name='wrf-edit-chem-data'),
    url(r'^wrf/new/popup-chem-data$', 'popup_new_task_chem_data', name='wrf_popup_new_task_chem_data'),
    url(r'^wrf/list-chem-data/$', 'list_chem_data', name='wrf_list_chem_data'),
    
    url(r'^wrf/list-meteo-data/$', 'list_meteo_data', name='wrf_list_meteo_data'),
    url(r'^wrf/list-model-setting/$', 'list_model_setting', name='wrf_list_model_setting'),
)

urlpatterns += patterns('aqm_web.views.plot',
    url(r'^plot/mercator$', 'mercator', name='map-preview-mercator'),
    url(r'^plot/lambert-conformal$', 'lambert_conformal'),
    url(r'^plot/test$', 'test_plot'),
    url(r'^plot/grads/wrf/(\d+)/(\d+)/$', 'grads_wrf_plot', name='grads-wrf-plot'),
    url(r'^plot/wrf/domain/(\d+)/$', 'wrf_domain_map', name='map-domain-preview'),
)

# REST API
auth = CookieAuthentication(realm="AQM Web Interface")
ad = { 'authentication': auth }

serverstatus_resource = Resource(handler=handlers_wrf.ServerStatusHandler, **ad)
server_resource = Resource(handler=handlers_wrf.ServerHandler, **ad)
task_resource = Resource(handler=handlers_wrf.TaskHandler, **ad)
task_control_resource = Resource(handler=handlers_wrf.TaskControlHandler, **ad)
chemdata_resource = Resource(handler=handlers_wrf.ChemDataHandler, **ad)
m2m_resource = Resource(handler=handlers_wrf.M2MCommandHandler, **ad)
wrfgrads_resource = Resource(handler=handlers_wrf.GradsWRFHandler, **ad)

urlpatterns += patterns('',
    url(r'^rest/server/status/(?P<server_id>[^/]+)/$', serverstatus_resource, name='rest-server-utilization'),
    url(r'^rest/server/detail/$', server_resource, name='rest-server-detail-list'),
    url(r'^rest/server/detail/(?P<server_id>[^/]+)/$', server_resource, name='rest-server-detail'),
    url(r'^rest/task/$', task_resource, name='rest-task-list'),
    url(r'^rest/task/all/$', task_resource, kwargs={'task_id': None, 'all_user': True}, name='rest-task-list-all'), 
    url(r'^rest/task/detail/(?P<task_id>[^/]+)/$', task_resource, name='rest-task'),
    url(r'^rest/task/control/$', task_control_resource, name='rest-task-control-list'),
    url(r'^rest/chemdata/$', chemdata_resource, name='rest-chemdata-list'),
    url(r'^rest/chemdata/all/$', chemdata_resource, kwargs={'chemdata_id': None, 'all_user': True}, name='rest-chemdata-list-all'),
    url(r'^rest/chemdata/detail/(?P<chemdata_id>[^/]+)/$', chemdata_resource, name='rest-chemdata-detail'),
    url(r'^rest/m2m/$', m2m_resource, name='rest-m2m'),
    url(r'^rest/grads/wrf/$', wrfgrads_resource, name='rest-wrf-grads-static'),
    url(r'^rest/grads/wrf/(?P<server_id>[^/]+)/(?P<envid>[^/]+)/(?P<domain>[^/]+)/$', wrfgrads_resource, name='rest-wrf-grads'),
)
