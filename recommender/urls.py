from django.urls import path
from . import views

urlpatterns = [
    path('', views.cover, name='cover'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recommendation/', views.recommendation_form, name='recommendation_form'),
    path('password-reset/', views.custom_password_reset, name='password_reset'),
    path('admin/login/', views.admin_login, name='admin_login'),  # For modal login
    path('dashboard/', views.dashboard, name='dashboard'),  # Your custom dashboard
]