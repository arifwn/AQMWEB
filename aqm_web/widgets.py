# -*- coding: utf-8 -*-
#
# Created:    2010/09/09
# Author:         alisue
#
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

# check is configured correctly
if not hasattr(settings, "CODEMIRROR_PATH"):
    raise ImproperlyConfigured("You must define the CODEMIRROR_PATH before using the CodeMirrorTextarea.")

if settings.CODEMIRROR_PATH.endswith('/'):
    settings.CODEMIRROR_PATH = settings.CODEMIRROR_PATH[:-1]
    
class CodeMirrorTextarea(forms.Textarea):
    u"""Textarea widget render with `CodeMirror`
    
    CodeMirror:
        http://codemirror.net/
    """

    class Media:
        css = {'screen': ('%s/lib/codemirror.css' % settings.CODEMIRROR_PATH,) }
        js = (
            r"%s/lib/codemirror.js" % settings.CODEMIRROR_PATH,
            r"%s/mode/xml/xml.js" % settings.CODEMIRROR_PATH,
            r"%s/mode/css/css.js" % settings.CODEMIRROR_PATH,
            r"%s/mode/javascript/javascript.js" % settings.CODEMIRROR_PATH,
            r"%s/mode/htmlmixed/htmlmixed.js" % settings.CODEMIRROR_PATH,
        )
        
    def __init__(self, attrs=None, path=None, stylesheet=None, **kwargs):
        super(CodeMirrorTextarea, self).__init__(attrs=attrs, **kwargs)
        self.path = path or settings.CODEMIRROR_PATH
    
    def render(self, name, value, attrs=None):
        u"""Render CodeMirrorTextarea"""
        html = super(CodeMirrorTextarea, self).render(name, value, attrs)
        kwargs = {
            'id': "\"id_%s\""%name,
        }
        for key in kwargs.keys():
            kwargs[key] = mark_safe(kwargs[key])
        code = render_to_string(r"sidebar/codemirror.html", kwargs)
        body = "%s\n%s" % (html, code)
        return mark_safe(body)
    
class AdminCodeMirrorTextareaWidget(CodeMirrorTextarea, AdminTextareaWidget):
    u"""CodeMirrorTextarea for Admin site"""
    pass
