from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.homepage ,name="home"),
    path('<slug:slug>/products', views.product_list ,name="product_list"),
    path('product/<slug:slug>',views.product_view, name="product_view"),
    path('search/',views.search_results, name="search"),
    path('filter-data',views.filter_data,name='filter_data'),
    # path('<slug:slug>/<str:slug2>/products', views.sub_category ,name="sub_category"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

