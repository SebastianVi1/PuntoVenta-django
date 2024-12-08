from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout_view'),
    path('', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('modify_product/<uuid:id_unico>/', views.modify_product, name='modify_product'),
    path('delete_product/<uuid:id_unico>/', views.delete_product, name='delete_product'),
    path('ventas/', views.ventas, name='ventas'),
    path('reporte-ventas/', views.reporte_ventas, name='reporte-ventas'),
    path('eliminar-todas-ventas/', views.eliminar_todas_ventas, name='eliminar_todas_ventas'),
    path('users/', views.listar_usuarios, name='users'),
    path('register/', views.register_user, name='register_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    
]
