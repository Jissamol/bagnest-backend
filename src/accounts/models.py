from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.timezone import now
from django.db import models

from django.db import models

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    last_name = models.CharField(max_length=128, blank=True, null=True, default='')
    mobile = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=False, default='default@example.com')
    address = models.CharField(max_length=1024, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_separated = models.BooleanField(default=False)  # Add this field with a default value

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name


# models.py in your Django app


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()  # Stock quantity from the seller
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

# src/accounts/models.py

#
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(default=now)  # Ensure added_at exists
#
#     def total_price(self):
#         return self.product.price * self.quantity
#
#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"
