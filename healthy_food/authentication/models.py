# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    #email = models.EmailField(unique=True)

    # 'username' => identifiant de connexion
    # USERNAME_FIELD = 'username'
    # 'email' requis à la création
    # REQUIRED_FIELDS = ['email']

    # objects = CustomUserManager()

    def __str__(self):
        return self.username

