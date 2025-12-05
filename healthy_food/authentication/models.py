# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    def __str__(self):
        return self.username


