from django.shortcuts import render

import random

quotes = ["The ability to play chess is the sign of a gentleman. The ability to play chess well is the sign of a wasted life.", "I am more strongly confirmed than ever in the belief that the time devoted to chess is literally frittered away.", "Help your pieces so they can help you.", "Chess is eminently and emphatically the philospher's game."]

images = ["https://upload.wikimedia.org/wikipedia/commons/b/b2/PaulCharlesMorphy.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/53/Paul_Morphy_standing_New_York_1859.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/bb/Morphy_L%C3%B6wenthal_1858.jpg", "https://upload.wikimedia.org/wikipedia/commons/f/f0/Paul_Morphy.jpg"]

# Create your views here.
def quote(request):
    '''Respond to the main page/ quote request'''
    template_name = "quotes/quote.html"
    return render(request, template_name, {"quote": random.choice(quotes), "image": random.choice(images)})

def show_all(request):
    '''Respond to the show all quotes request'''
    template_name = "quotes/show_all.html"
    return render(request, template_name, {"quotes": quotes, "images": images})

def about(request):
    '''Respond to the about request'''
    template_name = 'quotes/about.html'
    return render(request, template_name)