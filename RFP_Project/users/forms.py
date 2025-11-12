# forms.py
from django import forms
from .models import Users, VendorDetails

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        model = Users
        fields = ['first_name','last_name','email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = VendorDetails
        exclude = ['user']