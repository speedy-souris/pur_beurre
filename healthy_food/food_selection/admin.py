from django.contrib import admin
from food_selection.models import Product, Category


# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutriscore')


admin.site.register(Product, ProductsAdmin)
admin.site.register(Category)
