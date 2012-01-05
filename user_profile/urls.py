'''
Created on Jan 5, 2012

@author: arif
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^profile/([-\w]+)$', 'user_profile.views.view_profile', name='view-profile'),
    
    # handle user login
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change'),
    url(r'^change_password_done/$', 'django.contrib.auth.views.password_change_done'),
    
)
