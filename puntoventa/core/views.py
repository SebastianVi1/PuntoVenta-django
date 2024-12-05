from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from productos.forms import ProductoForm

# Create your views here.
def home(request):
    return render(request, 'core/base.html')

def login(request):
    return render(request, 'core/login.html')

def sales(request):
    return render(request, 'core/inventory.html')

def inventory(request):
    productos = Producto.objects.all()
    return render(request, 'core/inventory.html', {'productos':productos})

def modify_product(request, id_unico):
     # Obtiene el producto o lanza un error 404 si no existe
    producto = get_object_or_404(Producto, id_unico=id_unico)
    if request.method == 'POST':
        # Actualizar los campos del producto con los nuevos datos
        producto.nombre = request.POST.get('nombre_producto', producto.nombre)
        producto.precio = request.POST.get('precio_producto', producto.precio)
        producto.categoria = request.POST.get('categoria_producto', producto.categoria)
        producto.stock = request.POST.get('stock_producto', producto.stock)
        producto.descripcion = request.POST.get('descripcion_productos', producto.descripcion)
        # Convertir el precio a formato decimal (reemplazar coma por punto)
        
        
        # Guardar los cambios en la base de datos
        producto.save()
        # Redirigir a la página de detalles o la lista de productos
        return redirect('modify_product', producto_id=producto.id_unico)
    return render(request, 'core/modify_product.html', {'producto':producto})


