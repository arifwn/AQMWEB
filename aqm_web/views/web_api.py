'''
Created on Nov 24, 2011

@author: arif
'''
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson as json
from django.core.cache import cache


def get_server_utilization(request, server_id):
    from aqm_utils.xmlrpc import Client
    
    if request.user.is_anonymous():
        return HttpResponseForbidden()
        
    server_addr_key = 'server_addr_%s' % server_id
    server_addr = cache.get(server_addr_key, None)
    if server_addr is None:
        # TODO: read server info from db
        addr = '127.0.0.1'
        port = 8080
        server_addr = 'https://%s:%d' % (addr, port)
        cache.set(server_addr_key, server_addr)
    
    
    server_utilization_key = 'server_utilization_%s' % server_id
    server_utilization = cache.get(server_utilization_key, None)
    if server_utilization is None:
        c = Client(server_addr)
        try:
            server_utilization = c.server.utilization()
        except:
            resp = HttpResponse()
            resp.status_code = 503
            return resp
        
        cache.set(server_utilization_key, server_utilization, 5)
    
    json_str = json.dumps(server_utilization)
    return HttpResponse(json_str)
    