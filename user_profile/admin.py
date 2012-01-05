'''
Created on Dec 14, 2011

@author: arif
'''
from user_profile.models import Profile
from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    
admin.site.register(Profile, ProfileAdmin)
