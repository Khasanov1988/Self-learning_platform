from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Remove the username field and replace it with email as the unique identifier
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')  # Email field for authentication
    FIO = models.CharField(max_length=100, verbose_name='Full Name', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='Phone Number', null=True, blank=True)
    comment = models.CharField(max_length=150, verbose_name='Comment', null=True, blank=True)

    # Specify 'email' as the field used for authentication
    USERNAME_FIELD = 'email'

    # No additional fields are required during registration
    REQUIRED_FIELDS = []
