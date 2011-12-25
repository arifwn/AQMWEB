from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AQMWebInterface.views.home', name='home'),
    # url(r'^AQMWebInterface/', include('AQMWebInterface.foo.urls')),
    
    url(r'^grappelli/', include('grappelli.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
#     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # the main web interface
    url(r'^', include('aqm_web.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    