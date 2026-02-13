from django.urls import path
from .views import ProfileListView, ProfileDetailView
urlpatterns = [
    path('', ProfileListView.as_view() , name='profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile' ),
]