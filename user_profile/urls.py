'''
Created on Jan 5, 2012

@author: arif
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('user_profile.views',
    url(r'^profile/([-\w]+)$', 'view_profile', name='view-profile'),
    url(r'^edit/avatar$', 'edit_avatar', name='edit-avatar'),
    url(r'^edit/profile$', 'edit_profile', name='edit-profile'),
)

# handle user login
urlpatterns += patterns('django.contrib.auth.views',   
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout_then_login'),
    url(r'^change_password/$', 'password_change'),
    url(r'^change_password_done/$', 'password_change_done'),
    
)

# Misc. Helper views
urlpatterns += patterns('user_profile.views',
    url(r'^avatar/t32x32/([-\w]+)$', 'avatar_t32x32', name='user-avatar-t32x32'),
    url(r'^anon-avatar/t32x32$', 'avatar_t32x32', name='anon-avatar-t32x32'),
)