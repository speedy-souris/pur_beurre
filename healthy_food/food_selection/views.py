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
    search_form = SearchNewFood(request.GET or None)
    context = {'search_form': search_form, 'page_name': 'Résultats', 'page_obj': []}

    if not search_form.is_valid() or not search_form.cleaned_data.get('product'):
        return render(request, 'food_selection/products.html', context)

    product_name = search_form.cleaned_data['product']
    context['name'] = product_name

    possible_products = Product.objects.filter(name__icontains=product_name)

    if possible_products.exists():
        original_product = possible_products.first()

        context.update({
            'product_found': True,
            'required_product': original_product,
        })

        original_product_categories = original_product.categories.all()

        if original_product_categories.exists():
            alternative_products = Product.objects.filter(
                categories__in=original_product_categories,
                nutriscore__lt=original_product.nutriscore
            ).exclude(pk=original_product.pk).distinct().order_by('nutriscore')

            paginator = Paginator(alternative_products, 6)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            for product_in_page in page_obj:
                initial_data = {'product_id': product_in_page.pk}
                product_in_page.form = SaveProductForm(initial=initial_data)

            context['page_obj'] = page_obj

    else:
        context['product_found'] = False
        context['error_message'] = f"Aucun produit ne correspond à votre recherche '{product_name}'."

    return render(request, 'food_selection/products.html', context)


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
