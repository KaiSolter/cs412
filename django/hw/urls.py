from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

# url patterns for the hw app
urlpatterns = [
    #path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about, name="about_page"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)