from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    phone = models.CharField(max_length=9)
    adress = models.TextField(max_length=100)
    city = models.TextField(max_length=30)
    postal_code = models.TextField(max_length=20)
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    


