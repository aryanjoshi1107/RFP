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
    def __init__(self, *args, category_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # setting queryset provided by the view, or fall back to all (avoids import at module load)
        if category_queryset is not None:
            self.fields['category'].queryset = category_queryset
        else:
            # doing a local import to avoid circular import at module import time
            from django.apps import apps
            Category = apps.get_model('category', 'Category')
            self.fields['category'].queryset = Category.objects.all()
        
        
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))