
from django import forms

class NewTaskForm(forms.Form):
    task_name = forms.CharField(label='Name', max_length=200)
    task_description = forms.CharField(label='Description',
                                       widget=forms.Textarea(attrs={
                                        'rows':'3'
                                        }))
    task_namelist_wrf = forms.CharField(label='WRF Namelist',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    task_namelist_wps = forms.CharField(label='WPS Namelist',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    task_namelist_arwpost = forms.CharField(label='ARWpost Namelist',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    