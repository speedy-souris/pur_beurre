from django.shortcuts import render, get_object_or_404
from food_selection.forms import SearchNewFood, ContactUsForm
from food_selection.models import Product, Category


# Create your views here.
def home(request):
    form = SearchNewFood()
    return render(request,
                  'food_selection/home.html',
                  {'form': form})


def found(request):
    product_name, products_finded = '', ''
    if request.method == 'GET':
        form = SearchNewFood(request.GET)
        if form.is_valid():
            product_name = form.cleaned_data['product']
    else:
        form = get_object_or_404(SearchNewFood)
    products = Product.objects.filter(name__contains=product_name)
    for product in products:
        better_nutriscores = get_better_nutriscore_list(product.nutriscore)
        for category in product.categories.all():
            products_finded = Product.objects.filter(categories__name=category.name).\
                                              filter(nutriscore__in=better_nutriscores)
    context = {'name': product_name, 'products': products_finded, 'form': form}
    return render(request,
                  'food_selection/popular_products.html', context)


def recorded(request):
    return render(request, 'food_selection/recorded_product.html')


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
    if nutriscores.index(nutriscore) == 0:
        nutriscores_finded = nutriscores[0]
    else:
        nutriscores_finded = nutriscores[:nutriscores.index(nutriscore)]
    return nutriscores_finded
