"""
Module containing Celery tasks definitions
"""
# Pylint is unable to properly resolve packages without setting PYTHONENV
# pylint: disable=import-error, no-name-in-module
from celery import shared_task
from django.core.mail import send_mail
from .models import Product
from .serializers import ProductQuantitySerializer


@shared_task
def process_order(order_number, customer_email, product_map):
    """
    Process an order by deducting the specified product amount from the database
    and sending a confirmation email to the customer
    """
    for sku, quantity in product_map.items():
        product = Product.objects.get(pk=sku)  # pylint: disable=no-member
        updated_data = {"quantity": product.quantity - quantity}
        serializer = ProductQuantitySerializer(product, data=updated_data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError(f"Invalid data serialized: {updated_data}")

    send_mail(
        f"Order confirmation for order # {order_number}",
        f"This is to confirm that your order has been processed\nOrders:\n{product_map}",
        "test@test.com",
        [customer_email],
        fail_silently=False,
    )
