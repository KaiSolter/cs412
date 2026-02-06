from django.shortcuts import render
import random

daily_specials = ["Ribeye Steak", "Grilled Salmon", "Eggplant Parmesan"]

# Create your views here.

def main(request):
    '''Respond to the main page request'''
    template_name = "restaurant/main.html"
    return render(request, template_name )

def order(request):
    '''Respond to the order page request'''
    template_name = "restaurant/order.html"
    return render(request, template_name, context={'daily_special': random.choice(daily_specials)} )

def submit_order(request):
    '''Respond to the order submission'''
    template_name = "restaurant/order_confirmation.html"
    
    if request.POST:
        apps = request.POST.getlist('apps')
        
        entrees = request.POST.getlist('entrees')
        
        toppings = request.POST.getlist('toppings')
        
        ordered_toppings = False
        if len(toppings) > 0:
            ordered_toppings = True
        
        special = request.POST.getlist('special')
        
        ordered_special = False
        if len(special) > 0:
            ordered_special = True
        
        beverages = request.POST.getlist('beverages')
        
        instructions = request.POST['instructions']
        
        name = request.POST['order_name']
        
        phone_number = request.POST['phone_number']
    
    return render(request, template_name=template_name, context={
        'instructions': instructions, 'entrees': entrees, 'apps': apps, 'beverages': beverages, 'name': name, 'phone_number': phone_number, 'special': special, 'ordered_special': ordered_special, 'ordered_toppings': ordered_toppings, 'toppings': toppings, 'total': len(apps)*5 + len(entrees)*10 + len(beverages)*3 + (12 if ordered_special else 0) })