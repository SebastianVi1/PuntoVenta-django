from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from productos.forms import ProductoForm
from decimal import Decimal
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'core/base.html')

def login(request):
    return render(request, 'core/login.html')

def sales(request):
    return render(request, 'core/inventory.html')

def inventory(request):
    orden = request.GET.get('orden', 'nombre')
    if orden == 'precio':
        productos = Producto.objects.all().order_by('precio')  # Orden ascendente
    elif orden == 'categoria':
        productos = Producto.objects.all().order_by('categoria')
    elif orden == 'stock':
        productos = Producto.objects.all().order_by('-stock')  # Orden descendente
    else:
        productos = Producto.objects.all()


    return render(request, 'core/inventory.html', {'productos':productos})

def modify_product(request, id_unico):
     # Obtiene el producto o lanza un error 404 si no existe
    producto = get_object_or_404(Producto, id_unico=id_unico)
    
    if request.method == 'POST':

        

        # Actualizar los campos del producto con los nuevos datos
        producto.nombre = request.POST.get('nombre_producto', producto.nombre)
        producto.categoria = request.POST.get('categoria_producto', producto.categoria)
        producto.stock = request.POST.get('stock_producto', producto.stock)
        producto.descripcion = request.POST.get('descripcion_productos', producto.descripcion)

        precio_input = request.POST.get('precio_producto', str(producto.precio))
        try:
            producto.precio = Decimal(precio_input.replace(',', '.'))
        except:
            producto.precio = producto.precio  # Mantén el valor actual si hay error 


        #Guardar los cambios en la base de datos
        messages.success(request, f'{producto.nombre} Modificado con exito')
        producto.save()
        # Redirigir a la página de detalles o la lista de productos
        #return redirect('modify_product', id_unico=id_unico)  si queremos redirigir a el panel de modificacion
        return redirect('modify_product', id_unico=id_unico)
    return render(request, 'core/modify_product.html', {'producto':producto})

def delete_product(request, id_unico):
    producto = get_object_or_404(Producto, id_unico=id_unico)
    if request.method == 'POST':
        producto.delete()
        
        return redirect('inventory')
    