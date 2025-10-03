from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Producto, Categoria, Favorito, ImagenProducto
from .forms import ProductoForm

def explorar(request):
    """Vista principal para explorar productos"""
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    
    productos = Producto.objects.filter(estado='disponible').select_related(
        'categoria', 'vendedor'
    ).prefetch_related('imagenes')
    
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(tags__icontains=query)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    categorias = Categoria.objects.filter(activa=True)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
    }
    return render(request, 'productos/explorar.html', context)


@login_required
def detalle_producto(request, producto_id):
    """Vista detallada de un producto - SOLO para usuarios logueados"""
    producto = get_object_or_404(
        Producto.objects.select_related('categoria', 'vendedor').prefetch_related('imagenes'), 
        id=producto_id
    )
    
    # Incrementar visitas
    producto.incrementar_visitas()
    
    # Verificar si el usuario actual tiene este producto en favoritos
    es_favorito = False
    if hasattr(request.user, 'estudiante'):
        es_favorito = Favorito.objects.filter(
            estudiante=request.user.estudiante, 
            producto=producto
        ).exists()
    
    # Productos relacionados (misma categoría)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        estado='disponible'
    ).exclude(id=producto.id).select_related('categoria', 'vendedor')[:4]
    
    context = {
        'producto': producto,
        'es_favorito': es_favorito,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'productos/detalle.html', context)

@login_required
def toggle_favorito(request, producto_id):
    """Agregar o quitar producto de favoritos"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para usar favoritos")
        return redirect('productos:detalle', producto_id=producto_id)
    
    producto = get_object_or_404(Producto, id=producto_id)
    estudiante = request.user.estudiante
    
    try:
        favorito = Favorito.objects.get(estudiante=estudiante, producto=producto)
        favorito.delete()
        messages.success(request, "❌ Producto removido de favoritos")
    except Favorito.DoesNotExist:
        Favorito.objects.create(estudiante=estudiante, producto=producto)
        messages.success(request, "❤️ Producto agregado a favoritos")
    
    return redirect('productos:detalle', producto_id=producto_id)


@login_required
def mis_favoritos(request):
    """Mostrar todos los productos favoritos del usuario con estadísticas"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para ver favoritos")
        return redirect('productos:explorar')
    
    favoritos = Favorito.objects.filter(estudiante=request.user.estudiante).select_related(
        'producto', 'producto__categoria', 'producto__vendedor'
    ).prefetch_related('producto__imagenes')
    
    productos = [favorito.producto for favorito in favoritos]
    
    # Estadísticas MEJORADAS
    productos_disponibles = len([p for p in productos if p.estado == 'disponible'])
    precio_total = sum(p.precio for p in productos if p.estado == 'disponible')
    universidades_unicas = len(set(p.vendedor.universidad for p in productos if p.vendedor.universidad))
    
    # Categorías únicas para filtros
    categorias_favoritos = set(producto.categoria for producto in productos if producto.categoria)
    
    context = {
        'productos': productos,
        'productos_disponibles': productos_disponibles,
        'precio_total': precio_total,
        'universidades_unicas': universidades_unicas,
        'categorias_favoritos': categorias_favoritos,
        'titulo': 'Mis Favoritos'
    }
    return render(request, 'productos/mis_favoritos.html', context)

@login_required
def vender(request):
    """Vista para publicar un nuevo producto"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para vender productos")
        return redirect('productos:explorar')
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user.estudiante
            producto.save()
            
            # Manejar múltiples imágenes
            imagenes = request.FILES.getlist('imagenes')
            for i, imagen in enumerate(imagenes):
                ImagenProducto.objects.create(
                    producto=producto, 
                    imagen=imagen,
                    orden=i
                )
            
            messages.success(request, "🎉 ¡Producto publicado exitosamente!")
            return redirect('productos:detalle', producto_id=producto.id)
    else:
        form = ProductoForm()
    
    return render(request, 'productos/vender.html', {'form': form})

@login_required
def mis_productos(request):
    """Mostrar los productos del usuario actual"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para ver tus productos")
        return redirect('productos:explorar')
    
    productos = Producto.objects.filter(vendedor=request.user.estudiante)
    
    context = {
        'productos': productos,
        'titulo': 'Mis Productos'
    }
    return render(request, 'productos/mis_productos.html', context)

def productos_por_categoria(request, categoria_id):
    """Mostrar productos por categoría específica"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria, estado='disponible')
    
    context = {
        'productos': productos,
        'categoria': categoria,
        'titulo': f'Productos en {categoria.get_nombre_display()}'
    }
    return render(request, 'productos/explorar.html', context)

def iniciar_checkout(request, producto_id):
    """Inicia el proceso de checkout para un producto"""
    producto = get_object_or_404(Producto, id=producto_id, estado='disponible')

    if request.method == "POST":
        # Aquí podrías crear una orden real en tu modelo Order si lo tuvieras
        messages.success(request, f"🎉 Has comprado {producto.nombre} exitosamente.")
        return redirect("productos:detalle", producto_id=producto.id)

    context = {
        "producto": producto,
    }
    return render(request, "checkout/iniciar.html", context)

### vistas faltantes

@login_required
def editar_producto(request, producto_id):
    """Editar un producto existente"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar que el usuario es el vendedor
    if producto.vendedor != request.user.estudiante:
        messages.error(request, "No tienes permiso para editar este producto")
        return redirect('productos:mis_productos')
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            
            # Manejar nuevas imágenes
            imagenes = request.FILES.getlist('imagenes')
            for i, imagen in enumerate(imagenes):
                ImagenProducto.objects.create(
                    producto=producto, 
                    imagen=imagen,
                    orden=i
                )
            
            messages.success(request, "✅ Producto actualizado exitosamente")
            return redirect('productos:detalle', producto_id=producto.id)
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    """Eliminar un producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar que el usuario es el vendedor
    if producto.vendedor != request.user.estudiante:
        messages.error(request, "No tienes permiso para eliminar este producto")
        return redirect('productos:mis_productos')
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "🗑️ Producto eliminado exitosamente")
        return redirect('productos:mis_productos')
    
    return render(request, 'productos/eliminar.html', {'producto': producto})