'''
Created on Nov 24, 2011

@author: arif
'''
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

import namelist.encode
import namelist.decode

#TODO: return http 401 if not authenticated
def get_namelist(request, type):
    test_namelist = settings.MEDIA_ROOT + 'test_data/namelist.input'
    content_type = 'application/json'
    ext = 'json'
    
    data = namelist.decode.decode_namelist(test_namelist)
    
    if type == 'xml':
        ext = 'xml'
        content_type = 'text/xml'
        
        #TODO: return data as xml
        response = HttpResponse(simplejson.dumps(data), content_type='json')
    else:
        response = HttpResponse(simplejson.dumps(data), content_type=content_type)
    
    return response
