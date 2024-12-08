from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from productos.forms import ProductoForm
from decimal import Decimal
from django.contrib import messages
from .models import ReporteVenta
from django.db.models import Max
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required
def home(request):
    return render(request, 'core/base.html')

@login_required
def sales(request):
    return render(request, 'core/inventory.html')

@login_required
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

@login_required
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

@login_required
def delete_product(request, id_unico):
    producto = get_object_or_404(Producto, id_unico=id_unico)
    if request.method == 'POST':
        producto.delete()
        
        return redirect('inventory')
    
@login_required
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

@login_required
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
    
    return render(request, 'core/reporte-ventas.html', {
        'ventas_agrupadas': ventas_agrupadas
    })

@login_required
def eliminar_todas_ventas(request):
    if request.method == 'POST':
        ReporteVenta.objects.all().delete()
        return redirect('reporte_ventas')

@login_required 
def listar_usuarios(request):
    usuarios = User.objects.all()  # Obtiene todos los usuarios
    return render(request, 'core/users.html', {'usuarios': usuarios})

@login_required
def is_admin(user):
    return user.is_superuser


@login_required
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear usuario sin guardar aún
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Encripta la contraseña
            
            # Manejar campo personalizado `es_admin`
            if form.cleaned_data.get('es_admin'):
                user.is_staff = True  # Hacerlo administrador (puede acceder al panel admin)
            
            user.save()  # Guarda el usuario en la base de datos
            
            # Mensaje de éxito
            messages.success(request, "Usuario registrado con éxito.")
            return redirect('users')  # Redirige a la página de inicio de sesión
        else:
            # Si hay errores en el formulario
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = RegisterForm()
    
    return render(request, 'core/register.html', {'form': form})


@login_required
def delete_user(request, user_id):

    if not request.user.is_superuser:
        return redirect('users')  # Solo superusuarios pueden borrar usuarios
    
    user_to_delete = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('users')  # Redirigir después de borrar al listado de usuarios

    # Si no es un método POST, renderiza una confirmación
    return render(request, 'core/confirm_delete.html', {'user': user_to_delete})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Autenticar al usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirigir al 'next' si existe o al home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario inválido")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')