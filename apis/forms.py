from django import forms
from django.core import validators
from .models import UserData, ProductData
import phonenumbers
from django_countries import countries
import re
def validate_mobile_number(value):
    if len(value) != 10:
        raise forms.ValidationError("Mobile number should be 10 digits long.")
    
# using Form
class user_reg(forms.Form):
    name = forms.CharField(validators=[validators.MaxLengthValidator(20)])
    email = forms.EmailField(validators=[validators.EmailValidator()])
    mobile_number = forms.CharField(validators=[validate_mobile_number])

# using ModelForm

def validate_name(value):
    if re.search(r'\d', value):  
        raise forms.ValidationError("Name should not contain numbers.")
    
class modelUser_reg(forms.ModelForm):
    
    country_choices = []
    for code, name in countries:
        try:
            dial_code = phonenumbers.country_code_for_region(code)
            short_name = name[:3].upper()
            country_choices.append((code, f"{short_name} +{dial_code}"))
        except Exception:
            pass 
    country_code = forms.ChoiceField(choices=country_choices, label="Country")
    mobile_number = forms.CharField(max_length=15, label="Mobile number")
    name = forms.CharField(validators=[validators.MaxLengthValidator(20), validate_name])

    
    class Meta:
        model = UserData
        fields = ['name', 'email', 'country_code', 'mobile_number']
    
    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        mobile_number = cleaned_data.get('mobile_number')
        
        
        if not mobile_number or not country_code:
            raise forms.ValidationError("Both country code and mobile number are required.")
        try:
            country_dial_code = phonenumbers.country_code_for_region(country_code)
            
            full_number = f"+{country_dial_code}{mobile_number}"
            parsed_number = phonenumbers.parse(full_number, None)
            
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid mobile number.")
            
            cleaned_data['mobile_number'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except Exception as e:
            raise forms.ValidationError("Invalid country code.", e)
        
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductData
        fields = ['product_name', 'product_price', 'image']