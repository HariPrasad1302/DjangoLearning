from django import forms
from django.core import validators
from .models import UserData

def validate_mobile_number(value):
    if len(value) != 10:
        raise forms.ValidationError("Mobile number should be 10 digits long.")
    
# using Form
class user_reg(forms.Form):
    name = forms.CharField(validators=[validators.MaxLengthValidator(20)])
    email = forms.EmailField(validators=[validators.EmailValidator()])
    mobile_number = forms.CharField(validators=[validate_mobile_number])

# using ModelForm

class modelUser_reg(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['name', 'email', 'mobile_number']
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must be a number.")
        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits.")
        return mobile
