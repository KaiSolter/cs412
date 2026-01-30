from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def quote(request):
    '''Respond to the main page/ quote request'''
    template_name = "quotes/quote.html"
    return render(request, template_name)

def show_all(request):
    '''Respond to the show all quotes request'''
    template_name = "quotes/show_all.html"
    return render(request, template_name)

def about(request):
    '''Respond to the about request'''
    template_name = 'quotes/about.html'
    return render(request, template_name)