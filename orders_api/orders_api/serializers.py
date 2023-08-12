"""
Django serializers
"""
from rest_framework import serializers
from .models import Product


class ProductStatusSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Product status
    """
    class Meta:  # pylint: disable=missing-class-docstring
        model = Product
        fields = ["status"]


class ProductQuantitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Product quantity
    """
    class Meta:  # pylint: disable=missing-class-docstring
        model = Product
        fields = ["quantity"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Product objects
    """
    update_status = serializers.HyperlinkedIdentityField(view_name="update-product-status")
    deduct_stock = serializers.HyperlinkedIdentityField(view_name="deduct-product-quantity")

    class Meta:  # pylint: disable=missing-class-docstring
        model = Product
        fields = ["url", "name", "sku", "price", "description", "quantity", "status", "update_status", "deduct_stock"]
