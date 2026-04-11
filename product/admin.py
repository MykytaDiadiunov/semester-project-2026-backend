from django.contrib import admin
from .models.product import Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Product)

# Register your models here.
