# noinspection PyInterpreter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import SearchNewFood, ContactUsForm, SaveProductForm, TestForm
from .models import Product, Favorite


# Create your views here.
def home(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Accueil'
               }
    return render(request, 'food_selection/home.html', context)


def profile(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Profile'
               }
    return render(request, 'food_selection/profile.html', context)


def found(request):
    search_form = SearchNewFood(request.GET or None)
    context = {
        'search_form': search_form,
        'page_name': 'Résultats',
        'page_obj': [],
        'product_found': False
    }

    if not search_form.is_valid() or not search_form.cleaned_data.get('product'):
        return render(request, 'food_selection/products.html', context)

    product_name = search_form.cleaned_data['product']
    context['name'] = product_name

    possible_products = Product.objects.filter(name__icontains=product_name)

    if possible_products.exists():
        original_product = possible_products.first()

        context.update({'product_found': True, 'required_product': original_product})

        original_product_categories = original_product.categories.all()

        if original_product_categories.exists():
            alternative_products = Product.objects.filter(
                categories__in=original_product_categories,
                nutriscore__lt=original_product.nutriscore
            ).exclude(pk=original_product.pk).distinct().order_by('nutriscore')

            paginator = Paginator(alternative_products, 6)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            # On prépare le formulaire pour chaque produit
            for product_in_page in page_obj:
                initial_data = {'product_id': product_in_page.pk}
                product_in_page.form = SaveProductForm(initial=initial_data)

            context['page_obj'] = page_obj

    else:
        context['product_found'] = False
        context['message_vide'] = messages.error(request, "Aucun produit ne correspond à votre recherche.")
        return redirect('food_selection:home')

    return render(request, 'food_selection/products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'food_selection/product_detail.html'
    context_object_name = 'product'
    slug_field = "product_id"
    slug_url_kwarg = "product_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context.update({
            'page_name': 'Détails du produit',
            'nutriments': product.nutriments,
            'search_form': SearchNewFood(),
        })
        return context


def contact(request):
    context = {'search_form': SearchNewFood(),
               'contact_form': ContactUsForm(),
               'page_name': 'Contact'}
    return render(request, 'food_selection/contact.html', context)


def disclaimer(request):
    context = {'search_form': SearchNewFood(),
               'page_name': 'Mentions légales'
               }
    return render(request, 'food_selection/legal_disclaimer.html', context)


# MODIFICATION IMPORTANTE ICI : Utilisation de Favorite et LoginRequiredMixin
class SaveProductFormView(LoginRequiredMixin, FormView):
    template_name = "food_selection/products.html"
    form_class = SaveProductForm
    success_url = "/saved_products_list/"

    def form_valid(self, form):
        product_id = form.cleaned_data.get('product_id')

        # On récupère le produit de manière sécurisée
        product = get_object_or_404(Product, pk=product_id)

        # On crée le lien Favori entre l'utilisateur connecté et le produit
        # get_or_create évite les doublons si l'utilisateur clique 2 fois
        Favorite.objects.get_or_create(user=self.request.user, product=product)

        return super().form_valid(form)

    # Si l'utilisateur n'est pas connecté, on lui dit
    def handle_no_permission(self):
        messages.error(self.request, "Vous devez être connecté pour sauvegarder un produit.")
        return super().handle_no_permission()


# MÊME LOGIQUE POUR LE TEST
class TestFormView(LoginRequiredMixin, FormView):
    template_name = "food_selection/test_form.html"
    form_class = TestForm
    success_url = '/saved_products_list/'

    def form_valid(self, form):
        product_id = form.cleaned_data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        Favorite.objects.get_or_create(user=self.request.user, product=product)

        return super().form_valid(form)


# MODIFICATION IMPORTANTE ICI : On liste les Favoris, pas les Produits
class SavedProductsListView(LoginRequiredMixin, ListView):
    model = Favorite  # On change le modèle de base
    paginate_by = 6
    template_name = 'food_selection/saved_products.html'
    context_object_name = 'favorites'  # On renomme pour être clair dans le template

    def get_queryset(self):
        # On retourne uniquement les favoris de l'utilisateur connecté
        # select_related('product') optimise la requête SQL (évite de requêter le produit pour chaque ligne)
        return Favorite.objects.filter(user=self.request.user).select_related('product').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchNewFood(),
            'page_name': 'Mes Favoris',
        })
        return context

    def handle_no_permission(self):
        messages.error(self.request, "Vous devez être connecté pour voir les favoris.")
        return super().handle_no_permission()