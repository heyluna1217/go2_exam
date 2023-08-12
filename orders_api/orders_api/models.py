"""
Django db model representation of API resources
"""
from django.db import models


class Product(models.Model):
    """
    Product resource model
    """
    name = models.CharField()
    sku = models.CharField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    status = models.BooleanField()
