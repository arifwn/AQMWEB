
from django import forms
from tinymce.widgets import TinyMCE

class NewTaskForm(forms.Form):
    task_name = forms.CharField(label='Name', max_length=200)
    task_description = forms.CharField(label='Description',
                                       widget=TinyMCE(mce_attrs={
                                                        'theme': "advanced",
                                                        'plugins': "inlinepopups",
                                                        'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,blockquote,bullist,numlist,link,unlink,image,cleanup",
                                                        'theme_advanced_buttons2' : "",
                                                        'theme_advanced_buttons3' : "",
                                                        'theme_advanced_toolbar_location' : "top",
                                                        'theme_advanced_toolbar_align' : "right"
                                                        }))
    hillheight_setting = forms.CharField(label='HillHeight Generator Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    wrf2aermod_setting = forms.CharField(label='Meteorological Data Extractor Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    aermet_setting = forms.CharField(label='AERMET Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    aermod_setting = forms.CharField(label='AERMOD Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    aermod2grads_setting = forms.CharField(label='AERMOD Result Processor Setting',
                                           widget=forms.Textarea(attrs={
                                            'rows':'10'
                                            }))
    
    grads_template = forms.CharField(label='GrADS Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    wrf_task_id = forms.IntegerField(label='WRF Task')
    
    