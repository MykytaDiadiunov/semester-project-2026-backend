from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "item_category"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name
