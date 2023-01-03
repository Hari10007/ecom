from django.urls import path, include
from . import views


urlpatterns = [
    path('apply_coupon', views.apply_coupon ,name="apply_coupon"),
    path('remove_coupon/<str:cart_id>', views.remove_coupon, name="remove_coupon"),
]