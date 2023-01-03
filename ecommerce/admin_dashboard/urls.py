from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dash'),
    path('admin_dashboard/category', views.category_list, name='category_list'),
    path('admin_dashboard/category_create', views.category_create, name='category_create'),
    path('admin_dashboard/<category_id>/category_update', views.category_update, name='category_update'),
    path('admin_dashboard/<category_id>/category_delete', views.category_delete, name='category_delete'),
    path('admin_dashboard/product', views.product_list, name='product_list'),
    path('admin_dashboard/product_create', views.product_create, name='product_create'),
    path('admin_dashboard/<product_id>/product_update', views.product_update, name='product_update'),
    path('admin_dashboard/<product_id>/product_delete', views.product_delete, name='product_delete'),
    path('admin_dashboard/customer', views.customer_list, name='customer_list'),
    path('admin_dashboard/<customer_id>/customer_block', views.customer_block, name='customer_block'),
    path('admin_dashboard/order', views.order_list, name='order_list'),
    path('admin_dashboard/<order_id>/order_update', views.order_update, name='order_update'),
    path('admin_dashboard/refund/<str:order_no>', views.refund, name="refund"),
    path('export/sales', views.export_sales_xls, name='export_sales'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
