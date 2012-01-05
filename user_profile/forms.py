'''
Created on Jan 5, 2012

@author: arif
'''

from django import forms

class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)


class AvatarEditForm(forms.Form):
    avatar = forms.ImageField()
    