'''
Created on Dec 14, 2011

@author: arif
'''
from wrf.models import ChemData, PollutantParam, AltMeteoData, Task, Setting, BaseSetting, TaskGroup, TaskQueue
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django import forms
from tinymce.widgets import TinyMCE

class SettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created', 'modified', 'is_removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(SettingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(Setting, SettingAdmin)

class BaseSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created', 'modified', 'is_removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseSettingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(BaseSetting, BaseSettingAdmin)

class PollutantParamAdmin(admin.ModelAdmin):
    list_display = ['pollutant',]
        
admin.site.register(PollutantParam, PollutantParamAdmin)

class ChemDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ChemDataAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(ChemData, ChemDataAdmin)

class AltMeteoDataAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'data_type', 'is_removed']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(AltMeteoDataAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(AltMeteoData, AltMeteoDataAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created', 'modified']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(Task, TaskAdmin)


class TaskQueueAdmin(admin.ModelAdmin):
    list_display = ['task', 'server', 'created', 'envid', 'status',
                    'stage', 'is_error']
        
admin.site.register(TaskQueue, TaskQueueAdmin)


class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['description'].widget = TinyMCE(mce_attrs={
            'plugins': "autolink,lists,pagebreak,advhr,advimage,advlink,emotions,inlinepopups,insertdatetime,media,searchreplace,paste,fullscreen,noneditable,visualchars,nonbreaking,",
            'theme': "advanced",
            'cleanup_on_startup': False,
            'custom_undo_redo_levels': 30,
            'theme_advanced_buttons1' : ",bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,outdent,indent,blockquote,bullist,numlistlink,unlink,image,media,|,formatselect,|,cleanup,code",
            'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,insertdate,inserttime,|,forecolor,backcolor,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,|,cite,abbr,acronym,attribs,|,visualchars,nonbreaking,blockquote,pagebreak,|,fullscreen",
            'theme_advanced_buttons3' : "",
            'theme_advanced_toolbar_location' : "top",
            'theme_advanced_toolbar_align' : "left",
            'theme_advanced_statusbar_location' : "bottom",
            'theme_advanced_resizing': True,
            }, )
        
        return form
        
admin.site.register(TaskGroup, TaskGroupAdmin)

