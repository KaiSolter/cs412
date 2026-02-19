from django.urls import path
from .views import *
urlpatterns = [
    path('', ProfileListView.as_view() , name='profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile' ),
    path('post/<int:pk>', PostDetailView.as_view(), name='post' )
]