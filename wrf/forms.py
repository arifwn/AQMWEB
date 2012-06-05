
from django import forms
from tinymce.widgets import TinyMCE

class NewTaskForm(forms.Form):
    '''
    This is temporary form for debugging purpose.
    Namespace and grads template retrieved from client should not be trusted.
    '''
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
    
    task_grads_template = forms.CharField(label='GrADS Template',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    