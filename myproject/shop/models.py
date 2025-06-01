import os
from django.db import models
from django.contrib.auth.models import User

def get_image_upload_path(instance, filename):
    # Store images in the 'media/products/<category_name>/<filename>'
    return os.path.join('products', instance.category.name, filename)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default='default-slug')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Image is stored in a folder based on the category name
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlisted_by')

    def __str__(self):
        return f"Wishlist of {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_id = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
