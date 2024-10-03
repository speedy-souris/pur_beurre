from django.db import models
from django.db.models import Model
# Create your models here.


class Category(models.Model):
    name = models.fields.CharField(max_length=10000, primary_key=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.fields.CharField(max_length=200)
    nutriscore = models.fields.CharField(max_length=1)
    product_id = models.fields.CharField(max_length=25, primary_key=True)
    categories = models.ManyToManyField(Category)
    url = models.fields.URLField(max_length=500)
    # image = models.fields.files.ImageField(upload_to='images')
    image = models.fields.URLField(max_length=500)

    def __str__(self):
        return f'{self.name}'

