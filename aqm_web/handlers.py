''' REST API handler '''

from django.utils import simplejson as json
from django.core.cache import cache

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from aqm_utils.xmlrpc import Client
from aqm_web.models import Server


class ServerStatusHandler(BaseHandler):
    ''' Get status of modelling servers '''
    methods_allowed = ('GET',)

    def read(self, request, server_id):
        server_addr_key = 'server_addr_%s' % server_id
        server_addr = cache.get(server_addr_key, None)
        if server_addr is None:
            # TODO: read server info from db
            try:
                srv = Server.objects.get(pk=server_id)
            except Server.DoesNotExist:
                return rc.NOT_FOUND
                
            server_addr = 'https://%s:%d' % (srv.address, srv.port)
            cache.set(server_addr_key, server_addr)
        
        server_utilization_key = 'server_utilization_%s' % server_id
        server_utilization = cache.get(server_utilization_key, None)
        if server_utilization is None:
            c = Client(server_addr)
            try:
                server_utilization = c.server.utilization()
            except:
                # remote server not available at the moment
                return rc.INTERNAL_ERROR
            
            cache.set(server_utilization_key, server_utilization, 5)
        
        return server_utilization