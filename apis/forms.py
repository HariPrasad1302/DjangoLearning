from django import forms
from django.core import validators


def validate_mobile_number(value):
    if len(value) != 10:
        raise forms.ValidationError("Mobile number should be 10 digits long.")
    

class user_reg(forms.Form):
    name = forms.CharField(validators=[validators.MaxLengthValidator(20)])
    email = forms.EmailField(validators=[validators.EmailValidator()])
    mobile_number = forms.CharField(validators=[validate_mobile_number])
    