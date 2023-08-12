"""
Django views
"""
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Product
from .serializers import (ProductQuantitySerializer, ProductSerializer,
                          ProductStatusSerializer)
from .tasks import process_order


class ListProducts(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    View for listing all products and creating new ones
    """

    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all products
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new product
        """
        return self.create(request, *args, **kwargs)


class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    View for fetching specific product instances and updating them
    """

    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Fetch specific product given its SKU
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Update an existing product
        """
        return self.update(request, *args, **kwargs)


class UpdateProductStatus(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    View for updating a specific product's status
    """

    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductStatusSerializer

    def patch(self, request, *args, **kwargs):
        """
        Update a product's status
        """
        return self.update(request, *args, **kwargs)


class CreateOrder(APIView):
    """
    View for creating an order and sending an asynchronous job to celery to fulfill it
    """

    def post(self, request):
        """
        Processes an order:
            1. Confirm if each item is still in stock
            2. Kick off an asynchronous Celery task
            3. Return the celery task ID as a response
        """
        item_list = request.data["items"]
        item_quantity_map = dict()
        for item in item_list:
            sku = item["sku"]
            try:
                product = Product.objects.get(pk=sku)  # pylint: disable=no-member
            except Product.DoesNotExist:  # pylint: disable=no-member
                return Response(status=status.HTTP_404_NOT_FOUND)

            if product.quantity <= 0:
                error_detail = {"detail": f"Item SKU {product.sku} is out of stock."}
                return Response(error_detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif item["quantity"] > product.quantity:
                error_detail = {
                    "detail": f"Order quantity for SKU {product.sku} is less than current stock: {product.quantity}"
                }
                return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)

            item_quantity_map[sku] = item["quantity"]

        order_number = request.data["order_number"]
        customer_email = request.data["customer"]["email"]

        async_result = process_order.delay(order_number, customer_email, item_quantity_map)

        response_detail = {"detail": f"Processing order with id {async_result.id}"}

        return Response(response_detail, status=status.HTTP_202_ACCEPTED)


class DeductProductQuantity(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    View for reducing a product's quantity
    """

    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductQuantitySerializer

    def patch(self, request, *args, **kwargs):
        """
        Update a product's quantity by deducting the specified amount
        """
        instance = self.get_object()
        if (update_quantity := request.data["quantity"]) > instance.quantity:
            error_detail = {
                "detail": f"Item quantity to deduct is greater than the current quantity {instance.quantity}."
            }
            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)

        request.data["quantity"] = instance.quantity - update_quantity

        return self.update(request, *args, **kwargs)


class AvailableProducts(mixins.ListModelMixin, generics.GenericAPIView):
    """
    View for listing all available products
    """

    queryset = Product.objects.filter(status=True).all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all available products
        """
        return self.list(request, *args, **kwargs)


class UnavailableProducts(mixins.ListModelMixin, generics.GenericAPIView):
    """
    View for listing all unavailable products
    """

    queryset = Product.objects.filter(status=False).all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all unavailable products
        """
        return self.list(request, *args, **kwargs)


@api_view(["GET"])
def api_root(request, format=None):
    """
    View for the root index
    """
    return Response(
        {
            "All products": reverse("products-list", request=request, format=format),
            "Available products": reverse("available-products-list", request=request, format=format),
            "Unavailable products": reverse("unavailable-products-list", request=request, format=format),
            "Create order": reverse("create-order", request=request, format=format),
        }
    )
