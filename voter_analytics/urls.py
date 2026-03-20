# voter_analytics/urls.py
# Kai Solter 2026-03-20
 
from django.urls import path
from . import views 
 
urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
]