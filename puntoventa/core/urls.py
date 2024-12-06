
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('inventory/', views.inventory, name='inventory'),

    path('modify_product/<uuid:id_unico>/', views.modify_product, name='modify_product'),
    path('delete_product/<uuid:id_unico>/', views.delete_product, name='delete_product'),
    path('register/', views.register, name='register')
]
