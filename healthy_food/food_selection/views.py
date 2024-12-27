from django.shortcuts import render, get_object_or_404
from food_selection.forms import SearchNewFood, ContactUsForm
from food_selection.models import Product, Category
from django.core.paginator import Paginator


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
    product = Product.objects.filter(name__contains=product_name).first()
    if not product:
        product_found = False
        return render(request, 'food_selection/popular_products.html', {'product_found': product_found})
    better_nutriscores = get_better_nutriscore_list(product.nutriscore)
    category_list = [category.name for category in product.categories.all()]
    alternative_products = Product.objects.filter(categories__name__in=category_list).\
                                                  filter(nutriscore__in=better_nutriscores)

    paginator = Paginator(alternative_products, 6)  # Show 6 products per page.
    page_number = request.GET.get("page", 1)

    print(f'page number = {page_number}')
    page_obj = paginator.get_page(page_number)
    context = {'name': product_name, 'products': alternative_products, 'form': form, "page_obj": page_obj, 'product_found': True}
    return render(request,
                  'food_selection/popular_products.html', context)


def recorded(request):
    product_found = found(request)
    return render(request, 'food_selection/recorded_product.html', {'products': product_found})


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

