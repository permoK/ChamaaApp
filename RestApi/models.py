# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('Mobile number is required')
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile_number, password, **extra_fields)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    sacco_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'"
    )
    mobile_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    username = None
    
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'sacco_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} - {self.sacco_name}"
