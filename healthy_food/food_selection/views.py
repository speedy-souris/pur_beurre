# noinspection PyInterpreter
from django.contrib.admin.templatetags.admin_list import search_form
from django.shortcuts import render, get_object_or_404
from food_selection.forms import SearchNewFood, ContactUsForm, SaveProductForm, TestForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from food_selection.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic.list import ListView


# Create your views here.
def home(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Accueil'
                }
    return render(request,'food_selection/home.html',context)


def found(request):
    product_name = ''
    if request.method == 'GET':
        search_form = SearchNewFood(request.GET)
        if search_form.is_valid():
            product_name = search_form.cleaned_data['product']
            print(f'nom produit = {product_name}')
    else:
        search_form = get_object_or_404(SearchNewFood)
    product = Product.objects.filter(name__contains=product_name).first()
    print(f"produit trouvé = {product}")
    if not product:
        product_found = False
        context = {
            'product_found': product_found,
            'search_form': SearchNewFood(),
        }
        return render(request, 'food_selection/products.html', context)
    better_nutriscores = get_better_nutriscore_list(product.nutriscore)
    print(f'nutriscore = {better_nutriscores} ')
    category_list = [category.name for category in product.categories.all()]
    print(f'categorie = {category_list}')
    alternative_products = Product.objects.filter(categories__name__in=category_list,
                                                  nutriscore__in=better_nutriscores).order_by('nutriscore')
    print(f'produits alternatif ={alternative_products}')
    paginator = Paginator(alternative_products, 6)  # Show 6 products per page.
    page_number = request.GET.get("page", 1)
    print(f'page number = {page_number}')
    page_obj = paginator.get_page(page_number)
    for general_product in page_obj:
        general_product.form = SaveProductForm(initial={'product_id': general_product.product_id})

    context = {
        'name': product_name,
        'products': alternative_products,
        'search_form': search_form,
        "page_obj": page_obj,
        'product_found': True,
        'page_name': 'Résultats',
        'required_product': product,
    }
    print(f'context ={context}')
    return render(request,'food_selection/products.html', context)


def recorded(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(pk=product_id)
    product.saved = True
    product.save()
    context = {
        'product': product,
        'page_name': 'Enregistrement',
    }
    print(f'produit enregistré')
    return render(request, 'food_selection/recorded_product.html', context)


def profile(request):
    context = {'page_name': 'Mon compte',
               'search_form': SearchNewFood(),
               }
    return render(request, 'food_selection/profile.html', context)

def contact(request):
    context = {'search_form': SearchNewFood(),
               'contact_form': ContactUsForm(),
               'page_name': 'Contact'}
    return render(request,'food_selection/contact.html', context)


def disclaimer(request):                         
    context = {'search_form': SearchNewFood(),
               'page_name': 'Mentions légales'
               }
    return render(request, 'food_selection/legal_disclaimer.html', context)


def get_better_nutriscore_list(nutriscore):
    """replace a bad nutriscore with better nutriscores (e.g. nutriscore D replaced with nutriscore list A, B, C)"""
    nutriscores = ['A', 'B', 'C', 'D', 'E']
    if nutriscores.index(nutriscore) == 0:
        nutriscores_finded = nutriscores[0]
    else:
        nutriscores_finded = nutriscores[:nutriscores.index(nutriscore)]
    return nutriscores_finded


class SaveProductFormView(FormView):
    template_name = "food_selection/products.html"
    form_class = SaveProductForm
    success_url = "/saved_products_list/"

    def form_valid(self, form):
        product_id = form.cleaned_data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            pass
        else:
            print(f'product_id = {product}')
            product.saved = True
            product.save()
        return super().form_valid(form)

class TestFormView(FormView):
    template_name = "food_selection/test_form.html"
    form_class = TestForm
    success_url = '/saved_products_list/'
    # success_url = reverse_lazy("saved")

    def form_valid(self,form):
        product_id = form.cleaned_data.get('product_id')
        print(f'id produit = {product_id}')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            pass
        else:
            print(f'product_id = {product}')
            product.saved = True
            product.save()

        return super().form_valid(form)

class SavedProductsListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'food_selection/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.filter(saved=True)
        paginator = Paginator(context['object_list'], 6)  # Show 6 products per page.
        page_number = self.request.GET.get("page", 1)
        print(f'page number = {page_number}')
        page_obj = paginator.get_page(page_number)
        context['page_name'] = 'Mes Aliments'
        context['search_form'] = SearchNewFood()
        context['page_obj'] = page_obj

        print(f"object_list = {context['object_list']}")
        return context
