from django.shortcuts import render
from food_selection.forms import SearchNewFood, ContactUsForm

# Create your views here.
def home(request):
    form = SearchNewFood()
    return render(request,
                  'food_selection/home.html',
                  {'form': form})

def recorded(request):
    return render(request, 'food_selection/recorded_product.html')

def profile(request):
    return render(request, 'food_selection/profile.html')

def contact(request):
    form = ContactUsForm()
    return render(request,
                  'food_selection/contact.html',
                  {'form': form})

def disclaimer(request):
    return render(request, 'food_selection/legal_disclaimer.html')
