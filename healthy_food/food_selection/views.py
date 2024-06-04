from django.shortcuts import render, get_object_or_404
from food_selection.forms import SearchNewFood, ContactUsForm
from food_selection.models import Product, Category


# Create your views here.
def home(request):
    form = SearchNewFood()
    return render(request,
                  'food_selection/home.html',
                  {'form': form})


def recorded(request):
    category_1 = ''
    if request.method == 'GET':
        form = SearchNewFood(request.GET)
        if form.is_valid():
            category_1 = form.cleaned_data['product']
    else:
        form = get_object_or_404(SearchNewFood)
    nutriscore_1 = get_better_nutriscore_list('C')
    print(f'nutriscore recherché = {nutriscore_1}')
    context = ''
    for n in nutriscore_1:
        print(n)
        products = Product.objects.all().filter(nutriscore__contains=n, categories__name=category_1)
        print(f'products = {products}')
        context = {'nom': 'produit recherché', 'products': products, 'form': form}
        print(f'context = {context}')
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
                  {'form': form, 'contact_form' : contact_form})


def disclaimer(request):
    form = SearchNewFood()
    return render(request, 'food_selection/legal_disclaimer.html',
                  {'form': form})


def get_better_nutriscore_list(nutriscore):
    """replace a bad nutriscore with the list of better nutriscores (e.g. nutriscore D replaced with list A , B, C)"""
    nutriscores = ['A', 'B', 'C', 'D', 'E']
    nutriscores_finded = nutriscores[:nutriscores.index(nutriscore)]
    return nutriscores_finded

