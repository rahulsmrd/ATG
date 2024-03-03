from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from home.models import *
from django import forms

class UserCreateForm(UserCreationForm):
    class Meta():
        fields = ('username','email','password1','password2')
        model=get_user_model()

        widgets={
            'username':forms.TextInput(attrs={
                'placeholder':"Username",
                'class':'form-control',
            }),
            'email':forms.EmailInput(attrs={
                'placeholder':"Email",
                'class':'form-control',
            }),
            'password1':forms.PasswordInput(attrs={
                'placeholder':"Password",
                'class':'form-control',
            }),
            'password2':forms.PasswordInput(attrs={
                'placeholder':"Password Confirmation",
                'class':'form-control',
            })
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control','onblur':'myfunc()'})
    

class profile_form(forms.ModelForm):
    class Meta():
        model=profile
        fields=('first_name', 'last_name','picture','address','city','state','pin','is_doctor','doc_id',)

        widgets={
            'first_name':forms.TextInput(attrs={
                'placeholder':'Name',
                'class':'form-control',
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder':'Picture',
                'class':'form-control',
            }),
            'picture':forms.FileInput(attrs={
                'placeholder':'Picture',
                'class':'form-control',
            }),
            'address':forms.TextInput(attrs={
                'placeholder':'Address',
                'class':'form-control',
            }),
            'city':forms.TextInput(attrs={
                'placeholder':'City/Town',
                'class':'form-control',
            }),
            'state':forms.TextInput(attrs={
                'placeholder':'State',
                'class':'form-control',
            }),
            'pin':forms.NumberInput(attrs={
                'placeholder':'Pin Code',
                'class':'form-control',
            }),
            'doc_id':forms.NumberInput(attrs={
                'placeholder':'Doctor Code',
                'class':'form-control',
            }),
            'is_doctor':forms.CheckboxInput(attrs={
                'onclick':'myfun()',
            }),
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_doctor'].label = 'Are you a Doctor ?'
        self.fields['doc_id'].label = 'Doctor Code'
    

class contact_form(forms.ModelForm):
    class Meta():
        model = contact_model
        fields="__all__"
        widgets={
            'name': forms.TextInput(
                attrs={
                    'placeholder':'Full Name',
                    'class': 'form-control',
                       }),
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'Email Address',
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(attrs={
                'placeholder':'Enter your concern to Contact us',
                'class': 'form-control',
                'row':15,
                'col':50,
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].label = 'Your Concern to Contact'