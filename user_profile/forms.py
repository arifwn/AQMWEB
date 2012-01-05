'''
Created on Jan 5, 2012

@author: arif
'''

from django import forms

class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, blank=True)
    last_name = forms.CharField(max_length=30, blank=True)
    email = forms.EmailField(blank=True)


class AvatarEditForm(forms.Form):
    avatar = forms.IntegerField()
    