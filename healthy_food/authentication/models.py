# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('SUBSCRIBER', 'Abonné'),
    ]

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        verbose_name='Rôle',
        default='SUBSCRIBER'
    )

    def __str__(self):
        return self.username


