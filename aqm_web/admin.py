'''
Created on Dec 14, 2011

@author: arif
'''
from aqm_web.models import Server
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django import forms


class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'user', 'address', 'port']

        
admin.site.register(Server, ServerAdmin)

