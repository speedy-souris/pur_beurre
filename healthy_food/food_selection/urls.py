from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from food_selection import views
from food_selection.views import  SavedProductsListView, ProductDetailView


app_name = 'food_selection'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('found/', views.found, name='found'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('profile/', views.profile, name='profile'),
    path('contact-us/', views.contact, name='contact'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('test_form/', views.TestFormView.as_view(), name='test-form'),
    path("save_products/", views.SaveProductFormView.as_view(), name="save_products"),
    path("saved_products_list/", SavedProductsListView.as_view(), name="saved-list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
