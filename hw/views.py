from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.
def home(request):
    '''Respond to the home request'''
    response_text = f'''
    <html>
    <h1>Hello, World!</h1>
    The current time is {time.ctime()}.
    </html>'''
    return HttpResponse(response_text)

def home_page(request):
    '''repond to the home request with template'''
    template_name = 'hw/home.html'
    context = {
        "time" : time.ctime(),
        "lette1" : chr(random.randint(65, 90 )),
        "lette2" :  chr(random.randint(65, 90 )),
        "number" : random.randint(1,10)
    }
    return render(request, template_name, context) 

def about(request):
    '''repond to the home request with template'''
    template_name = 'hw/about.html'
    context = {
        "time" : time.ctime(),
        "lette1" : chr(random.randint(65, 90 )),
        "lette2" :  chr(random.randint(65, 90 )),
        "number" : random.randint(1,10)
    }
    return render(request, template_name, context) 