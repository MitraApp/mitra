from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    conf_password = forms.CharField(label='Repeat Password', max_length=100)
