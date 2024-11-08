from django.db import models

# Create your models here.
from django.db import models
from bagnestapp.models import User
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Cart of {self.user.username}"
