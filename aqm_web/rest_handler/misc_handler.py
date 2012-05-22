
from piston.handler import BaseHandler
from piston.utils import rc, throttle

import aqm_utils.server
from aqm_utils.xmlrpc import Client
from aqm_web.models import Server


class ServerStatusHandler(BaseHandler):
    ''' Get status of modelling servers '''
    methods_allowed = ('GET',)

    def read(self, request, server_id):
        try:
            status = aqm_utils.server.get_status(server_id)
        except aqm_utils.server.ServerDoesNotExist:
            return rc.NOT_FOUND
        except IOError:
            return rc.THROTTLED
        except:
            return rc.INTERNAL_ERROR
        
        return status
    
    def create(self, request, server_id):
        return rc.FORBIDDEN
    
    def update(self, request, server_id):
        return rc.FORBIDDEN
    
    def delete(self, request, server_id):
        return rc.FORBIDDEN

class ServerHandler(BaseHandler):
    ''' Get RPC server list and details. '''
    model = Server
    methods_allowed = ('GET',)
    fields = ('id', 'name', 'address', 'port', 'is_enabled',
              'get_rest_url', 'get_status_rest_url')
    
    def read(self, request, server_id=None):
        if server_id is not None:
            try:
                return Server.objects.get(pk=server_id)
            except Server.DoesNotExist:
                return rc.NOT_FOUND
            except ValueError:
                return rc.BAD_REQUEST
        else:
            return Server.objects.filter(is_enabled=True).all()
    
    def create(self, request, server_id=None):
        return rc.FORBIDDEN
    
    def update(self, request, server_id=None):
        return rc.FORBIDDEN
    
    def delete(self, request, server_id=None):
        return rc.FORBIDDEN
