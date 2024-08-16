from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.fields.CharField(max_length=10000)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.fields.CharField(max_length=100)
    nutriscore = models.fields.CharField(max_length=1)
    categories = models.ManyToManyField(Category)
    url = models.fields.URLField(max_length=500)

    def __str__(self):
        return f'{self.name}'

