from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('login/', views.user_login, name='login'),
    path('sign_up/', views.user_create, name='sign_up'),
    path('otp_login/', views.otp_login, name='otp_login'),
    path('otp_verification/<str:id>/<str:secret>', views.otp_verification, name='otp_verification'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

