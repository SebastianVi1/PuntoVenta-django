from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/base.html')

def login(request):
    return render(request, 'core/login.html')

def products(request):
    return render(request, 'core/productos.html')