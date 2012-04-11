'''
Custom Piston Authentication module
'''
from django.contrib.auth import authenticate

from piston.authentication import HttpBasicAuthentication


class CookieAuthentication(HttpBasicAuthentication):
    ''' This authentication handler will first try to read user auth
        from request.user, if it doesn't exist fallback to http basic auth.
    '''
    def __init__(self, auth_func=authenticate, realm='API'):
        self.auth_func = auth_func
        self.realm = realm
    
    def is_authenticated(self, request):
        try:
            if request.user.is_authenticated():
                return True
        except AttributeError:
            pass
        
        return super(CookieAuthentication, self).is_authenticated(request)
        