# noinspection PyInterpreter
from django.contrib.admin.templatetags.admin_list import search_form
from django.views.generic.detail import DetailView
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
            print(f'nom produit recherché = {product_name}')
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
    print(f'nutriscore du produit trouvé = {better_nutriscores} ')
    category_list = [category.name for category in product.categories.all()]
    print(f'categorie du produit trouvé = {category_list}')
    alternative_products = Product.objects.filter(categories__name__in=category_list,
                                                  nutriscore__in=better_nutriscores).order_by('nutriscore')
    print(f'produits alternatif trouvé ={alternative_products}')
    paginator = Paginator(alternative_products, 6)  # Show 6 products per page.
    page_number = request.GET.get("page", 1)
    print(f'page number des produits trouvés = {page_number}')
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
    print(f'context des produits trouvés ={context}')
    return render(request,'food_selection/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'food_selection/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # Récupère l'objet actuel
        context['page_name'] = 'Détails du produit'
        context['nutriments'] = product.nutriments  # Utilise l'instance
        context['search_form'] = SearchNewFood()
        print(context)
        return context


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
            print(f'product_id formView = {product_id}')
            product.saved = True
            product.save()
            print(f'produit enregistré')
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
    template_name = 'food_selection/saved_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.filter(saved=True).order_by('name')
        paginator = Paginator(context['object_list'], 6)  # Show 6 products per page.
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context = {
            page_obj.number: page_obj.number,
            'search_form': SearchNewFood(),
            'page_obj': page_obj,
            'page_name': 'Mes Favoris',
        }
        print(f'page_obj = {context["page_obj"]}')
        return context
