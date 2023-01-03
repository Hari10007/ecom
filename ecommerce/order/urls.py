from django.urls import path, include
from . import views


urlpatterns = [
    path('order/checkout', views.checkout, name="checkout"),
    path('order/payment', views.payment, name="payment"),
    path('place_order', views.placeOrder, name="place_order"),
    path('proceed-to-pay', views.razorPay, name="proceed-to-pay"),
    path('order/thank_you', views.thankYou, name="thank_you"),
    path('my_orders', views.index, name="my_orders"),
    path('save_pdf/<str:order_no>', views.save_pdf, name="save_pdf"),
    path('cancel_order/<str:order_no>', views.cancel_order, name="cancel_order"),
    path('order_details/<str:order_no>', views.order_details, name= "order_details"),
]