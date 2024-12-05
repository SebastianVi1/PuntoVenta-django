
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('inventory/', views.inventory, name='inventory'),
    path('sales/', views.sales, name='sales'),
    path('modify_product/<uuid:id_unico>/', views.modify_product, name='modify_product'),
    path('delete_product/<uuid:id_unico>/', views.delete_product, name='delete_product')
]
