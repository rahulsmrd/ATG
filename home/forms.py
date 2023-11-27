from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from home.models import *
from django import forms

class UserCreateForm(UserCreationForm):
    class Meta():
        fields = ('username','email','password1','password2')
        model=get_user_model()

        help_texts = {
            'username': "</br><span style='margin:0 7em' class='fs-6'>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>",
            'password2': "</br><span style='margin:0 6.6em'>Enter the same password as before, for verification.</span>",
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'

class profile_form(forms.ModelForm):
    class Meta():
        model=profile
        fields=('first_name', 'last_name','picture','address','city','state','pin','is_doctor',)

        widgets={
            'picture':forms.FileInput(attrs={
                'placeholder':'Picture',
            }),
        }