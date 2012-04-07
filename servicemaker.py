'''
Run Django 1.4 using Twisted WSGI container

foreground: twistd -n --reactor=epoll rundjserver
background (demonized): twistd --reactor=epoll rundjserver

Created on Jan 22, 2012

@author: arif
'''

import os
from django.conf import settings

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor, ssl

from aqmwebinterface import wsgi as django_wsgi


DEBUG = getattr(settings, 'DEBUG', True)
DEFAULT_ADDR = getattr(settings, 'RUNSERVER_DEFAULT_ADDR', '')
DEFAULT_PORT = getattr(settings, 'RUNSERVER_DEFAULT_PORT', '8000')
SSL_KEY = getattr(settings, 'SSL_CERT_KEY')
SSL_CERT = getattr(settings, 'SSL_CERT_CERT')


class Options(usage.Options):
    optParameters = [["port", "p", DEFAULT_PORT, "The port number to listen on."],
                     ["address", "a", DEFAULT_ADDR, "The address to listen on."],
                     ["servestatic", "s", 'yes', "Serve Static content directly from Twisted."]]

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource
    
    
class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()


class AQMServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "rundjserver"
    description = "Django Application Server"
    options = Options

    def makeService(self, options):
        
        # make a new MultiService to hold the thread/web services
        multi = service.MultiService()

        # make a new ThreadPoolService and add it to the multi service
        tps = ThreadPoolService(threadpool.ThreadPool())
        tps.setServiceParent(multi)

        # create the WSGI resource using the thread pool and Django handler
        resource = wsgi.WSGIResource(reactor, tps.pool, django_wsgi.application)
        # create a custom 'root' resource, that we can add other things to
        root = Root(resource)
        
        # serve the static media
        if (DEBUG is False) and (options['servestatic'] == 'yes'):
            static_resource = static.File(settings.STATIC_ROOT)
            media_resource = static.File(settings.MEDIA_ROOT)
            root.putChild(settings.STATIC_URL.strip('/'), static_resource)
            root.putChild(settings.MEDIA_URL.strip('/'), media_resource)
        
        site = server.Site(root)
        
        if((SSL_KEY is not None) and (SSL_CERT is not None)):
            sslcontext = ssl.DefaultOpenSSLContextFactory(SSL_KEY, SSL_CERT)
            ws = internet.SSLServer(int(options['port']), site, sslcontext, interface=options['address'])
        else:
            ws = internet.TCPServer(int(options['port']), site, interface=options['address'])
        
        # add the web server service to the multi service
        ws.setServiceParent(multi)
        return multi
