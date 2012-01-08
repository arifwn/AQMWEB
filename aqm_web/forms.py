'''
Created on Nov 7, 2011

@author: Arif
'''
from django import forms
from wrf.models import PollutantParam

# -- Chem Data Form --

class ChemDataForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
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
    
    