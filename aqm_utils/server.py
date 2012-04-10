

from django.core.cache import cache

from aqm_utils.xmlrpc import Client
from aqm_web.models import Server


ServerDoesNotExist = Server.DoesNotExist


def rpc_client(server_id, cached=True):
    ''' Return RPC Client for specified server id. '''
    
    server_addr_key = 'server_addr_%s' % server_id
    if cached:
        server_addr = cache.get(server_addr_key, None)
    else:
        server_addr = None
        
    if server_addr is None:
        # read server info from db
        srv = Server.objects.get(pk=server_id)
            
        server_addr = 'https://%s:%d' % (srv.address, srv.port)
        cache.set(server_addr_key, server_addr, 30)
    
    c = Client(server_addr)
    return c

def get_status(server_id, cached=True):
    ''' Return status for specified server id. '''
    
    server_utilization_key = 'server_utilization_%s' % server_id
    if cached:
        server_utilization = cache.get(server_utilization_key, None)
    else:
        server_utilization = None
    
    if server_utilization is None:
        c = rpc_client(server_id, cached)
        try:
            server_utilization = c.server.utilization()
            server_utilization['id'] = server_id
        except:
            # remote server not available at the moment
            raise IOError()
        
        cache.set(server_utilization_key, server_utilization, 5)
    
    return server_utilization
