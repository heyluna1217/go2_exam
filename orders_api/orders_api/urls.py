"""
Django URLs
"""
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from .views import (AvailableProducts, CreateOrder, DeductProductQuantity,
                    ListProducts, ProductDetail, UnavailableProducts,
                    UpdateProductStatus, api_root)

schema_url_patterns = [
    path("products/", include("orders_api.urls")),
    path("orders/", include("orders_api.urls")),
]

urlpatterns = [
    path(
        "openapi",
        get_schema_view(
            title="Products API", description="API for managing orders", version="1.0.0", patterns=schema_url_patterns
        ),
        name="openapi-schema",
    ),
    path("", api_root),
    path("products/", ListProducts.as_view(), name="products-list"),
    path("products/available", AvailableProducts.as_view(), name="available-products-list"),
    path("products/unavailable", UnavailableProducts.as_view(), name="unavailable-products-list"),
    path("products/<int:pk>/", ProductDetail.as_view(), name="product-detail"),
    path("products/<int:pk>/deductstock", DeductProductQuantity.as_view(), name="deduct-product-quantity"),
    path("products/<int:pk>/status", UpdateProductStatus.as_view(), name="update-product-status"),
    path("orders/", CreateOrder.as_view(), name="create-order"),
    path(
        "swagger-ui/",
        TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
]
