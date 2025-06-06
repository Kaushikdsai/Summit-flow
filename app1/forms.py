from django import forms
from .models import User
from django.contrib.auth.forms import PasswordResetForm

class RegistrationForm(forms.Form):
    name=forms.CharField(max_length=150)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered!")
        return email

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        if password and confirm_password:
            if password!=confirm_password:
                raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class TimerForm(forms.Form):
    focus_duration=forms.TimeField()
    break_duration=forms.TimeField(required=False)
    websites=forms.CharField(required=False)

class CustomPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(max_length=254)
