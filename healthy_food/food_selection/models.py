from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    product_id = models.CharField(max_length=25, primary_key=True)
    categories = models.ManyToManyField(Category)
    url = models.URLField(max_length=500)
    image_url = models.URLField(blank=True, null=True)
    image_nutrition_url = models.URLField(blank=True, null=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
