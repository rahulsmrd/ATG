from django import forms
from blog.models import *

class create_form(forms.ModelForm):
    class Meta():
        model=post
        fields=('title', 'image','summary','content')

        widgets={
            'title': forms.TextInput(attrs={
                'placeholder':"Title",
                'class': 'form-control',
                }),
                'image': forms.FileInput(attrs={
                'class': 'form-control',
                }),
                'summary': forms.TextInput(attrs={
                'placeholder':"An Overview of the Post",
                'class': 'form-control',
                }),
                'content': forms.Textarea(attrs={
                'placeholder':"Description of the post",
                'rows':10,
                'class': 'form-control',
                }),
        }