"""
User Forms
"""
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm)
from django.contrib.auth import get_user_model


class CustomAuthenticationForm(AuthenticationForm):
    """Custom AuthenticationForm. extends AuthenticationForm.
     Add error classes for input fields"""
    error_css_class = 'error'
    required_css_class = 'required-field'


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form. Extends UserCreationForm.
     Add error classes for input fields"""
    error_css_class = 'error'
    required_css_class = 'required-field'

    class Meta:
        model = get_user_model()
        fields = ['email', 'name']
