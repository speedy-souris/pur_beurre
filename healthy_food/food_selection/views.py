# noinspection PyInterpreter
from django.views.generic.detail import DetailView
from django.shortcuts import render
from food_selection.forms import SearchNewFood, ContactUsForm, SaveProductForm, TestForm
from django.views.generic.edit import FormView
from food_selection.models import Product, Category
from django.core.paginator import Paginator
from django.views.generic.list import ListView


# Create your views here.
def home(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Accueil'
                }
    return render(request,'food_selection/home.html',context)


def profile(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Profile'
                }
    return render(request,'food_selection/profile.html',context)


def found(request):
    # Instantiate the form with GET data if present
    search_form = SearchNewFood(request.GET or None)
    # Retrieve the product name if the form is valid
    product_name = search_form.cleaned_data['product'] if search_form.is_valid() else ''
    # Search for the corresponding product
    product = Product.objects.filter(name__icontains=product_name).first()
    # If no products found
    if not product:
        context = {
            'product_found': False,
            'search_form': SearchNewFood(),
        }
        return render(request, 'food_selection/products.html', context)
    better_nutriscores = get_better_nutriscore_list(product.nutriscore)
    category_list = [category.name for category in product.categories.all()]
    alternative_products = Product.objects.filter(categories__name__in=category_list,
                                                  nutriscore__in=better_nutriscores).order_by('nutriscore')
    paginator = Paginator(alternative_products, 6)  # Show 6 products per page.
    page_number = request.GET.get("page", 1)
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
    return render(request,'food_selection/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'food_selection/product_detail.html'
    context_object_name = 'product'
    slug_field = "product_id"  # field used
    slug_url_kwarg = "product_id"  # URL parameter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # Retrieves the current object
        context.update({
            'page_name': 'Détails du produit',
            'nutriments': product.nutriments,  # Use the instance
            'search_form': SearchNewFood(),
        })
        return context


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
    return nutriscores[:max(1,nutriscores.index(nutriscore))]


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
            product.saved = True
            product.save()
        return super().form_valid(form)


class TestFormView(FormView):
    template_name = "food_selection/test_form.html"
    form_class = TestForm
    success_url = '/saved_products_list/'

    def form_valid(self,form):
        product_id = form.cleaned_data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            pass
        else:
            product.saved = True
            product.save()
        return super().form_valid(form)


class SavedProductsListView(ListView):
    model = Product
    paginate_by = 6  # directly here, no need to recreate the paginator
    template_name = 'food_selection/saved_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Returns only saved products, sorted by name
        return Product.objects.filter(saved=True).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchNewFood(),
            'page_name': 'Mes Favoris',
        })
        return context
