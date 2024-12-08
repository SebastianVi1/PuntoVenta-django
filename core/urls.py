
from django.urls import path
from . import views
from .views import ventas, reporte_ventas

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('inventory/', views.inventory, name='inventory'),
    path('sales/', views.sales, name='sales'),
    path('modify_product/<uuid:id_unico>/', views.modify_product, name='modify_product'),
    path('ventas/', views.ventas, name='ventas'),
    path('reporte-ventas/', reporte_ventas, name='reporte_ventas'),
    path('eliminar-todas-ventas/', views.eliminar_todas_ventas, name='eliminar_todas_ventas'),
    
]