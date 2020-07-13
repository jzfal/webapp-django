"""
create custome forms 
"""

from django import forms 
from .models import Comment

class EmailPostForm(forms.Form):
    """
    create custom form for sharing post by email 
    """
    # for each form class, it comes with a custom widget, can be overridden with the widget attribute, all fieldtypes come with their own validation 
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, 
                                widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # just indicate which model to build the form from 
        fields = ('name', 'email', 'body') # can add in a fields list or an exclude list

        
class SearchForm(forms.Form):
    query = forms.CharField()