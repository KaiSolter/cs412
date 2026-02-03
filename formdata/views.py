from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_form(reequest):
    template_name = 'formdata/form.html'
    return render(reequest, template_name)

def submit(request):
    
    template_name = 'formdata/confirmation.html'
    print(request)
    
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
    
    return render(request, template_name=template_name, context={
        'name': name, 'favorite_color': favorite_color })
    