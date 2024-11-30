from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/base.html')

def login(request):
    return render(request, 'core/login.html')

def products(request):
    return render(request, 'core/productos.html')

def inventory(request):
    return render(request, 'core/inventory.html')

def sales(request):
    return render(request, 'core/inventory.html')