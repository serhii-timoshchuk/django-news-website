"""
URLs for Users
"""
from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
    path('login/', views.loginpage_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('thanks/', views.thanks_view, name='after_registration_page'),
    path('activation/<hash1>/<hash2>',
         views.activation_view,
         name='activation_link'),
]
