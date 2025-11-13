# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='vendor', **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=30,unique=True,null= False)
    first_name = models.CharField(max_length=20,null= False)
    last_name = models.CharField(max_length=20,null= False)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('vendor', 'Vendor')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
    



    


class VendorDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    revenue = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    employee_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    pan_number = models.CharField(max_length=30, unique=True)
    gst_number = models.CharField(max_length=30, unique=True)
    is_approved = models.BooleanField(default=False)
    category = models.ForeignKey('category.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{10,15}$', 'Enter a valid phone number')]
    )

    def __str__(self):
        return f"VendorDetails for {self.user.email}"
    
    
    
    
    
    
