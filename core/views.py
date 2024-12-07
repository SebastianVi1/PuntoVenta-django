from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from productos.forms import ProductoForm
from decimal import Decimal
from .models import ReporteVenta
from django.db.models import Max

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


def ventas(request):
    productos = Producto.objects.all()
    carrito = request.session.get('carrito', [])
    total = Decimal(0)
    cambio = Decimal(0)
    monto_pagado = Decimal(0)

    if request.method == 'POST':
        delete_producto_id = request.POST.get('delete_producto_id')
        if delete_producto_id:
            delete_producto_id = int(delete_producto_id)
            carrito = [item for item in carrito if item['id'] != delete_producto_id]
            request.session['carrito'] = carrito

        update_producto_id = request.POST.get('update_producto_id')
        if update_producto_id:
            update_producto_id = int(update_producto_id)
            cantidad = int(request.POST.get('cantidad', 1))
            for item in carrito:
                if item['id'] == update_producto_id:
                    item['cantidad'] = cantidad
                    item['total_por_producto'] = float(item['precio'] * cantidad)
            request.session['carrito'] = carrito

        else:
            busqueda = request.POST.get('busqueda_producto')
            producto_seleccionado = None
            if busqueda:
                producto_seleccionado = Producto.objects.filter(nombre__icontains=busqueda).first()

            if producto_seleccionado:
                cantidad = int(request.POST.get('cantidad', 1))
                monto_pagado = Decimal(request.POST.get('monto_pagado', 0))

                producto_en_carrito = next((item for item in carrito if item['id'] == producto_seleccionado.id), None)

                if producto_en_carrito:
                    producto_en_carrito['cantidad'] += cantidad
                    producto_en_carrito['total_por_producto'] = float(producto_en_carrito['precio'] * producto_en_carrito['cantidad'])
                else:
                    carrito.append({
                        'id': producto_seleccionado.id,
                        'nombre': producto_seleccionado.nombre,
                        'precio': float(producto_seleccionado.precio),
                        'cantidad': cantidad,
                        'total_por_producto': float(producto_seleccionado.precio * cantidad)
                    })

                request.session['carrito'] = carrito

        total = sum(item['total_por_producto'] for item in carrito)
        total = Decimal(total)
        monto_pagado = Decimal(request.POST.get('monto_pagado', 0))
        cambio = monto_pagado - total

        if 'monto_pagado' in request.POST and monto_pagado >= total:
            ultimo_venta_id = ReporteVenta.objects.aggregate(Max('venta_id'))['venta_id__max'] or 0
            nuevo_venta_id = ultimo_venta_id + 1
            
            for item in carrito:
                ReporteVenta.objects.create(
                    venta_id=nuevo_venta_id,
                    producto_id=item['id'],
                    cantidad=item['cantidad'],
                    precio_unitario=Decimal(item['precio']),
                    total_por_producto=Decimal(item['total_por_producto']),
                    monto_pagado=monto_pagado,
                    cambio=cambio
                )
            request.session['carrito'] = []
            carrito = []
            return redirect('ventas')

    for item in carrito:
        item['total_por_producto'] = item['precio'] * item['cantidad']

    return render(request, 'core/ventas.html', {
        'productos': productos,
        'carrito': carrito,
        'total': float(total),
        'cambio': float(cambio)
    })

def reporte_ventas(request):
    ventas_agrupadas = {}
    ventas = ReporteVenta.objects.all()
    
    for venta in ventas:
        if venta.venta_id not in ventas_agrupadas:
            ventas_agrupadas[venta.venta_id] = {
                'items': [],
                'total_general': 0,
                'monto_pagado': 0,
                'cambio': 0,
                'fecha': venta.fecha
            }
        ventas_agrupadas[venta.venta_id]['items'].append(venta)
        ventas_agrupadas[venta.venta_id]['total_general'] += venta.total_por_producto
        ventas_agrupadas[venta.venta_id]['monto_pagado'] = venta.monto_pagado
        ventas_agrupadas[venta.venta_id]['cambio'] = venta.cambio
    
    return render(request, 'core/reporte_ventas.html', {
        'ventas_agrupadas': ventas_agrupadas
    })

def eliminar_todas_ventas(request):
    if request.method == 'POST':
        ReporteVenta.objects.all().delete()
        return redirect('reporte_ventas')