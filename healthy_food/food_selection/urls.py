from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = 'food_selection'
urlpatterns = [
    path('', views.home, name='home'),
    path('found/', views.found, name='found'),
    path('product/<str:product_id>/', views.ProductDetailView.as_view(), name='product'),
    path('profile/', views.profile, name='profile'),
    path('contact-us/', views.contact, name='contact-us'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    path('test_form/', views.TestFormView.as_view(), name='test-form'),
    path("save_products/", views.SaveProductFormView.as_view(), name="save_products"),
    path("saved_products_list/", views.SavedProductsListView.as_view(), name="saved-list"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
