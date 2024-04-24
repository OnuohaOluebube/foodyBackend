from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from uuid import uuid4

class User(AbstractUser):
    email = models.EmailField(unique=True)
