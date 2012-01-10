'''
Created on Nov 7, 2011

@author: Arif
'''
from django import forms
from wrf.models import PollutantParam
from tinymce.widgets import TinyMCE

# -- Chem Data Form --

class ChemDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=TinyMCE(mce_attrs={
                                                        'theme': "advanced",
                                                        'plugins': "inlinepopups",
                                                        'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,blockquote,bullist,numlist,link,unlink,image,cleanup",
                                                        'theme_advanced_buttons2' : "",
                                                        'theme_advanced_buttons3' : "",
                                                        'theme_advanced_toolbar_location' : "top",
                                                        'theme_advanced_toolbar_align' : "right"
                                                        }))
    data = forms.FileField(max_length=200)
    
    #should be populated by client js with json list of pollutant parameter ids
    parameters_json = forms.CharField(widget=forms.HiddenInput, required=False)


class PollutantParameterForm(forms.Form):
    pollutant =  forms.ChoiceField(choices=PollutantParam.PLT_TYPE)
    x_begin = forms.CharField(max_length=200)
    x_end = forms.CharField(max_length=200)
    y_begin = forms.CharField(max_length=200)
    y_end = forms.CharField(max_length=200)
    lat_begin = forms.CharField(max_length=200)
    lat_end = forms.CharField(max_length=200)
    lon_begin = forms.CharField(max_length=200)
    lon_end = forms.CharField(max_length=200)
    value_begin = forms.CharField(max_length=200)
    value_end = forms.CharField(max_length=200)
    conversion_factor = forms.FloatField()
    
    #should be populated by client js with selected data workspace
    worksheet = forms.IntegerField(widget=forms.HiddenInput, required=False)
    
    