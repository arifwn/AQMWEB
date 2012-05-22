'''
Created on Sep 18, 2011

@author: Arif
'''
from django.conf.urls.defaults import *
from piston.resource import Resource

from aqm_web.rest_handler import aermod_handler
from aqm_web.rest_handler import misc_handler
from aqm_web.rest_handler import wrf_handler

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
    url(r'^wrf/new/$', 'new_task', name='wrf-new-task'),
    url(r'^wrf/task/(\d+)/$', 'view_task', name='wrf-task-detail'),
    url(r'^wrf/task/$', 'list_task', name='wrf-task-list'),
    
    url(r'^wrf/new-group/$', 'new_task_group', name='wrf-new-task-group'),
    url(r'^wrf/task-group-details/$', 'task_group_detail', name='wrf-task-group-detail'),
    url(r'^wrf/list-task-group/$', 'list_task_group', name='wrf-list-task-group'),
    
    url(r'^wrf/new-chem-data/$', 'new_chem_data', name='wrf-new-chem-data'),
    url(r'^wrf/new-chem-data-step2/(\d+)$', 'new_chem_data_step2', name='wrf-new-chem-data-step2'),
    url(r'^wrf/edit-chem-data/(\d+)$', 'edit_chem_data', name='wrf-edit-chem-data'),
    url(r'^wrf/new/popup-chem-data$', 'popup_new_task_chem_data', name='wrf-popup-new-task-chem-data'),
    url(r'^wrf/list-chem-data/$', 'list_chem_data', name='wrf-list-chem-data'),
    
    url(r'^wrf/list-meteo-data/$', 'list_meteo_data', name='wrf-list-meteo-data'),
    url(r'^wrf/list-model-setting/$', 'list_model_setting', name='wrf-list-model-setting'),
)

urlpatterns += patterns('aqm_web.views.aermod_view',
    url(r'^aermod/new/$', 'new_task', name='aermod-new-task'),
    url(r'^aermod/task/(\d+)/$', 'view_task', name='aermod-task-detail'),
    url(r'^aermod/task/$', 'list_task', name='aermod-task-list'),
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

serverstatus_resource = Resource(handler=misc_handler.ServerStatusHandler, **ad)
server_resource = Resource(handler=misc_handler.ServerHandler, **ad)

urlpatterns += patterns('',
    url(r'^rest/server/status/(?P<server_id>[^/]+)/$', serverstatus_resource, name='rest-server-utilization'),
    url(r'^rest/server/detail/$', server_resource, name='rest-server-detail-list'),
    url(r'^rest/server/detail/(?P<server_id>[^/]+)/$', server_resource, name='rest-server-detail'),
)

wrf_task_resource = Resource(handler=wrf_handler.TaskHandler, **ad)
wrf_task_control_resource = Resource(handler=wrf_handler.TaskControlHandler, **ad)
wrf_chemdata_resource = Resource(handler=wrf_handler.ChemDataHandler, **ad)
wrf_grads_resource = Resource(handler=wrf_handler.GradsWRFHandler, **ad)
wrf_m2m_resource = Resource(handler=wrf_handler.M2MCommandHandler, **ad)

urlpatterns += patterns('',
    url(r'^rest/wrf/task/$', wrf_task_resource, name='rest-wrf-task-list'),
    url(r'^rest/wrf/task/all/$', wrf_task_resource, kwargs={'task_id': None, 'all_user': True}, name='rest-wrf-task-list-all'), 
    url(r'^rest/wrf/task/detail/(?P<task_id>[^/]+)/$', wrf_task_resource, name='rest-wrf-task'),
    url(r'^rest/wrf/task/control/$', wrf_task_control_resource, name='rest-wrf-task-control-list'),
    url(r'^rest/wrf/chemdata/$', wrf_chemdata_resource, name='rest-wrf-chemdata-list'),
    url(r'^rest/wrf/chemdata/all/$', wrf_chemdata_resource, kwargs={'chemdata_id': None, 'all_user': True}, name='rest-wrf-chemdata-list-all'),
    url(r'^rest/wrf/chemdata/detail/(?P<chemdata_id>[^/]+)/$', wrf_chemdata_resource, name='rest-wrf-chemdata-detail'),
    url(r'^rest/wrf/grads$', wrf_grads_resource, name='rest-wrf-grads-static'),
    url(r'^rest/wrf/grads/(?P<server_id>[^/]+)/(?P<envid>[^/]+)/(?P<domain>[^/]+)/$', wrf_grads_resource, name='rest-wrf-grads'),
    url(r'^rest/wrf/m2m/$', wrf_m2m_resource, name='rest-wrf-m2m'),
)

aermod_task_resource = Resource(handler=aermod_handler.TaskHandler, **ad)
aermod_task_control_resource = Resource(handler=aermod_handler.TaskControlHandler, **ad)

urlpatterns += patterns('',
    url(r'^rest/aermod/task/$', aermod_task_resource, name='rest-aermod-task-list'),
    url(r'^rest/aermod/task/all/$', aermod_task_resource, kwargs={'task_id': None, 'all_user': True}, name='rest-aermod-task-list-all'), 
    url(r'^rest/aermod/task/detail/(?P<task_id>[^/]+)/$', aermod_task_resource, name='rest-aermod-task'),
    url(r'^rest/aermod/task/control/$', aermod_task_control_resource, name='rest-aermod-task-control-list'),
)