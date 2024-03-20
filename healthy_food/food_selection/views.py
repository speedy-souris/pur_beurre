from django.shortcuts import render

# Create your views here.
def accueil(request):
    return render(request, 'food_selection/accueil.html')