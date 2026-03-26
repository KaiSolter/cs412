# File: quotes/urls.py
# Author: Kai Solter (ksolter@bu.edu), 1/30/2026 
# Description: URL patterns for Paul Morphy Quotes 
from django.urls import path
from quotes import views

# url patterns for the quotes app
urlpatterns = [
    path(r'', views.quote, name='quote'),
    path(r'quote/', views.quote, name='quote'),
    path(r'show_all/', views.show_all, name='show_all'),
    path(r'about/', views.about, name='about'),
]