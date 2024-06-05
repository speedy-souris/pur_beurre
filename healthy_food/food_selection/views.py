from django.shortcuts import render, get_object_or_404
from food_selection.forms import SearchNewFood, ContactUsForm
from food_selection.models import Product


# Create your views here.
def home(request):
    form = SearchNewFood()
    return render(request,
                  'food_selection/home.html',
                  {'form': form})


def recorded(request):
    category = ''
    if request.method == 'GET':
        form = SearchNewFood(request.GET)
        if form.is_valid():
            category = form.cleaned_data['product']
    else:
        form = get_object_or_404(SearchNewFood)
    better_nutriscores = get_better_nutriscore_list("A")
    products = Product.objects.filter(categories__name=category, nutriscore__in=better_nutriscores)
    context = {'name': 'produit recherché', 'products': products, 'form': form}
    return render(request,
                  'food_selection/recorded_product.html', context)


def profile(request):
    form = SearchNewFood()
    return render(request, 'food_selection/profile.html',
                  {'form': form})


def contact(request):
    form = SearchNewFood()
    contact_form = ContactUsForm()
    return render(request,
                  'food_selection/contact.html',
                  {'form': form, 'contact_form': contact_form})


def disclaimer(request):
    form = SearchNewFood()
    return render(request, 'food_selection/legal_disclaimer.html',
                  {'form': form})


def get_better_nutriscore_list(nutriscore):
    """replace a bad nutriscore with better nutriscores (e.g. nutriscore D replaced with nutriscore list A, B, C)"""
    nutriscores = ['A', 'B', 'C', 'D', 'E']
    nutriscores_finded = nutriscores[:nutriscores.index(nutriscore)+1]
    return nutriscores_finded
