from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('api/login/', views.LoginUser.as_view(), name='api-login'),
    path('login/', views.custom_login_view, name='login'),
    path('admin-home/', views.admin_home_page, name='admin-home'),
]
