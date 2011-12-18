'''
Created on Dec 14, 2011

@author: arif
'''
from wrf.models import ChemData, AltMeteoData, Domain, Task, Setting, TaskGroup
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django import forms

class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'setting_version', 'removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(SettingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(Setting, SettingAdmin)

class ChemDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'data_type', 'removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ChemDataAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(ChemData, ChemDataAdmin)

class AltMeteoDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'data_type', 'removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(AltMeteoDataAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(AltMeteoData, AltMeteoDataAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'width', 'height', 'parent']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(DomainAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(Domain, DomainAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'period_start', 'period_end']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(Task, TaskAdmin)


class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'running']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form
        
admin.site.register(TaskGroup, TaskGroupAdmin)

