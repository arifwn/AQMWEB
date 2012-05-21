
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
    
    meteorology_setting = forms.CharField(label='Meteorology Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    aermod_setting = forms.CharField(label='AERMOD Setting',
                                       widget=forms.Textarea(attrs={
                                        'rows':'10'
                                        }))
    
    plot_setting = forms.CharField(label='Plotter Setting',
                                           widget=forms.Textarea(attrs={
                                            'rows':'10'
                                            }))
    
    wrf_task_id = forms.IntegerField(label='WRF Task')
    
    def clean(self):
        cleaned_data = super(NewTaskForm, self).clean()
        
        # validate wrf task id
        from wrf.models import Task as WRFTask
        wrf_task_id = cleaned_data.get('wrf_task_id')
        try:
            wrf_task = WRFTask.objects.get(id=wrf_task_id)
            cleaned_data['wrf_task'] = wrf_task
        except WRFTask.DoesNotExist:
            msg = 'Cannot find specified WRF Task.'
            self._errors["wrf_task_id"] = self.error_class([msg])
            
            del cleaned_data['wrf_task_id']
        
        return cleaned_data