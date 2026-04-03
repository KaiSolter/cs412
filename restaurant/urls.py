# file restaurant/urls.py 
# Author: Kai Solter (ksolter@bu.edu), 2/3/2026
# Description: URL patterns for the restaurant assignment

from django.urls import path
from restaurant import views

#url patterns for the restaurant app
urlpatterns = [
    path(r'', views.main, name='main'),
    path(r'main/', views.main, name='main'),
    path(r'order/', views.order, name='order'),
    path(r'submit_order/', views.submit_order, name='submit_order'),   

]