from django.conf import settings
from django.db import models

class Category(models.Model):
    """ create and structure a table for the product category in the database """
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """ create and structure a table for a product in the database """
    product_id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    categories = models.ManyToManyField(Category)
    nutriments = models.JSONField(null=True)
    url = models.URLField(max_length=500)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    """ create and structure a link table between a user and a product in the database """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        """ create a unique relationship between a user and a product in the database """
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} aime le produit {self.product.name}"
