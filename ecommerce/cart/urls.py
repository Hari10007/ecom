from django.urls import path, include
from . import views


urlpatterns = [
    path('cart/edit', views.cart ,name="cart"),
    path('add_cart/<product_id>', views.add_cart ,name="add_cart"),
    path('increment_cart', views.increment_cart ,name="increment_cart"),
    path('decrement_cart', views.decrement_cart ,name="decrement_cart"),
    path('remove_cart_item/<product_id>', views.remove_cart_item ,name="remove_cart_item"),
    path('add_address', views.add_address, name="add_address"),
]