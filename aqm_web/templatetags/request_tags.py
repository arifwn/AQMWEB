'''
Created on Nov 4, 2011

@author: Arif
'''
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django import template

register = template.Library()

def query_string(request, variables, mode):
    variable_list = variables.split(' ')
    query_string_dict = {}
    for variable in variable_list:
        value = request.GET.get(variable, '')
        if value:
            query_string_dict[variable] = escape(value)
    if query_string_dict:
        if mode == "html_form":
            query_string = ' '.join([u'<input type="hidden" name="%s" value="%s">' % (k, v) for k, v in query_string_dict.items()])
        else:
            query_string = '?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in query_string_dict.items()]).replace(' ', '%20')
            if mode == "include_ampersand":
                query_string += '&amp;'
    else:
        if mode == "include_ampersand":
            query_string = '?'
        else:
            query_string = ''
    return mark_safe(query_string)

register.simple_tag(query_string)