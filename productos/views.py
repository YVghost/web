from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
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
    """Mostrar todos los productos favoritos del usuario con estadísticas y filtros"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para ver favoritos")
        return redirect('productos:explorar')
    
    favoritos = Favorito.objects.filter(estudiante=request.user.estudiante).select_related(
        'producto', 'producto__categoria', 'producto__vendedor'
    ).prefetch_related('producto__imagenes')
    
    # Aplicar filtros
    filtro_activo = request.GET.get('filtro', '')
    categoria_filtro = request.GET.get('categoria', '')
    
    productos_favoritos = []
    for favorito in favoritos:
        producto = favorito.producto
        # Aplicar filtro de estado
        if filtro_activo:
            if filtro_activo == 'disponible' and producto.estado != 'disponible':
                continue
            elif filtro_activo == 'reservado' and producto.estado != 'reservado':
                continue
            elif filtro_activo == 'vendido' and producto.estado != 'vendido':
                continue
            elif filtro_activo == 'nuevo' and not producto.es_nuevo:
                continue
        
        # Aplicar filtro de categoría
        if categoria_filtro and producto.categoria and producto.categoria.nombre != categoria_filtro:
            continue
            
        productos_favoritos.append(producto)
    
    # Estadísticas (sobre todos los favoritos, no solo los filtrados)
    todos_productos = [f.producto for f in favoritos]
    productos_disponibles = len([p for p in todos_productos if p.estado == 'disponible'])
    precio_total = sum(p.precio for p in todos_productos if p.estado == 'disponible')
    universidades_unicas = len(set(p.vendedor.universidad for p in todos_productos if p.vendedor.universidad))
    
    # Categorías únicas para filtros
    categorias_favoritos = set(producto.categoria for producto in todos_productos if producto.categoria)
    
    context = {
        'productos': productos_favoritos,
        'productos_disponibles': productos_disponibles,
        'precio_total': precio_total,
        'universidades_unicas': universidades_unicas,
        'categorias_favoritos': categorias_favoritos,
        'filtro_activo': filtro_activo,
        'categoria_filtro': categoria_filtro,
        'total_productos': len(todos_productos),
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
    """Mostrar los productos del usuario actual con filtros y estadísticas"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para ver tus productos")
        return redirect('productos:explorar')
    
    # Obtener todos los productos del usuario
    productos = Producto.objects.filter(vendedor=request.user.estudiante).select_related(
        'categoria'
    ).prefetch_related('imagenes').order_by('-publicado_en')
    
    # Aplicar filtros
    estado_filtro = request.GET.get('estado', '')
    categoria_filtro = request.GET.get('categoria', '')
    
    productos_filtrados = productos
    if estado_filtro and estado_filtro != 'todos':
        productos_filtrados = productos_filtrados.filter(estado=estado_filtro)
    
    if categoria_filtro:
        productos_filtrados = productos_filtrados.filter(categoria_id=categoria_filtro)
    
    # Organizar productos por estado para estadísticas
    productos_activos = productos.filter(estado='disponible')
    productos_reservados = productos.filter(estado='reservado')
    productos_vendidos = productos.filter(estado='vendido')
    productos_inactivos = productos.filter(estado='inactivo')
    
    # Estadísticas
    total_productos = productos.count()
    total_visitas = productos.aggregate(Sum('visitas'))['visitas__sum'] or 0
    total_favoritos = sum(producto.cantidad_favoritos for producto in productos)
    
    # Categorías únicas del usuario para filtros
    categorias_usuario = Categoria.objects.filter(
        productos__vendedor=request.user.estudiante
    ).distinct()
    
    context = {
        'productos': productos_filtrados,
        'productos_activos': productos_activos,
        'productos_reservados': productos_reservados,
        'productos_vendidos': productos_vendidos,
        'productos_inactivos': productos_inactivos,
        'total_productos': total_productos,
        'total_visitas': total_visitas,
        'total_favoritos': total_favoritos,
        'categorias_usuario': categorias_usuario,
        'estado_filtro': estado_filtro,
        'categoria_filtro': categoria_filtro,
    }
    return render(request, 'productos/mis_productos.html', context)

@login_required
def marcar_todos_vendidos(request):
    """Marcar todos los productos disponibles como vendidos"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Acceso denegado")
        return redirect('productos:mis_productos')
    
    if request.method == 'POST':
        productos_activos = Producto.objects.filter(
            vendedor=request.user.estudiante,
            estado='disponible'
        )
        
        count = productos_activos.update(estado='vendido')
        
        if count > 0:
            messages.success(request, f"✅ {count} productos marcados como vendidos")
        else:
            messages.info(request, "No hay productos disponibles para marcar como vendidos")
    
    next_url = request.POST.get('next', 'productos:mis_productos')
    return redirect(next_url)

@login_required
def estadisticas_productos(request):
    """Estadísticas detalladas de los productos del usuario"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante")
        return redirect('productos:explorar')
    
    productos = Producto.objects.filter(vendedor=request.user.estudiante)
    
    # Estadísticas básicas
    total_productos = productos.count()
    productos_por_estado = productos.values('estado').annotate(total=Count('id'))
    productos_por_categoria = productos.values('categoria__nombre').annotate(total=Count('id'))
    
    # Productos más populares
    productos_populares = productos.order_by('-visitas')[:5]
    
    # Estadísticas de tiempo
    from django.utils import timezone
    from datetime import timedelta
    
    ultima_semana = timezone.now() - timedelta(days=7)
    productos_recientes = productos.filter(publicado_en__gte=ultima_semana).count()
    
    context = {
        'total_productos': total_productos,
        'productos_por_estado': productos_por_estado,
        'productos_por_categoria': productos_por_categoria,
        'productos_populares': productos_populares,
        'productos_recientes': productos_recientes,
        'total_visitas': productos.aggregate(Sum('visitas'))['visitas__sum'] or 0,
        'total_favoritos': sum(p.cantidad_favoritos for p in productos),
    }
    return render(request, 'productos/estadisticas.html', context)

@login_required
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

### VISTAS ADICIONALES

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
    
    context = {
        'form': form, 
        'producto': producto,
        'imagenes_existentes': producto.imagenes.all()
    }
    return render(request, 'productos/editar.html', context)

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

@login_required
def cambiar_estado_producto(request, producto_id, nuevo_estado):
    """Cambiar el estado de un producto (vender, reservar, etc.)"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.vendedor != request.user.estudiante:
        messages.error(request, "No tienes permiso para modificar este producto")
        return redirect('productos:mis_productos')
    
    estados_permitidos = ['disponible', 'vendido', 'reservado', 'inactivo']
    if nuevo_estado not in estados_permitidos:
        messages.error(request, "Estado no válido")
        return redirect('productos:mis_productos')
    
    producto.estado = nuevo_estado
    producto.save()
    
    mensajes_estado = {
        'disponible': "🟢 Producto marcado como disponible",
        'vendido': "🔴 Producto marcado como vendido", 
        'reservado': "🟡 Producto marcado como reservado",
        'inactivo': "⚫ Producto marcado como inactivo"
    }
    
    messages.success(request, mensajes_estado.get(nuevo_estado, "Estado actualizado"))
    
    # Redirigir a la página anterior o a mis productos
    next_url = request.POST.get('next', request.GET.get('next', 'productos:mis_productos'))
    return redirect(next_url)

def productos_por_categoria(request, categoria_id):
    """Mostrar productos por categoría específica"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria, estado='disponible').select_related(
        'categoria', 'vendedor'
    ).prefetch_related('imagenes')
    
    context = {
        'productos': productos,
        'categoria': categoria,
        'titulo': f'Productos en {categoria.get_nombre_display()}'
    }
    return render(request, 'productos/explorar.html', context)

@login_required
def duplicar_producto(request, producto_id):
    """Duplicar un producto existente para crear uno nuevo basado en él"""
    producto_original = get_object_or_404(Producto, id=producto_id)
    
    # Verificar que el usuario es el vendedor
    if producto_original.vendedor != request.user.estudiante:
        messages.error(request, "No tienes permiso para duplicar este producto")
        return redirect('productos:mis_productos')
    
    # Crear una copia del producto
    producto_nuevo = Producto(
        nombre=f"Copia de {producto_original.nombre}",
        descripcion=producto_original.descripcion,
        categoria=producto_original.categoria,
        precio=producto_original.precio,
        condicion=producto_original.condicion,
        estado='disponible',
        stock=producto_original.stock,
        es_multiple=producto_original.es_multiple,
        tipo_envio=producto_original.tipo_envio,
        tags=producto_original.tags,
        vendedor=request.user.estudiante
    )
    producto_nuevo.save()
    
    # Copiar imágenes (opcional - si quieres duplicar las imágenes también)
    # for imagen in producto_original.imagenes.all():
    #     ImagenProducto.objects.create(
    #         producto=producto_nuevo,
    #         imagen=imagen.imagen,
    #         orden=imagen.orden
    #     )
    
    messages.success(request, "📋 Producto duplicado exitosamente. Ahora puedes editarlo.")
    return redirect('productos:editar', producto_id=producto_nuevo.id)

@login_required
def activar_desactivar_producto(request, producto_id):
    """Activar o desactivar un producto rápidamente"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.vendedor != request.user.estudiante:
        messages.error(request, "No tienes permiso para modificar este producto")
        return redirect('productos:mis_productos')
    
    # Cambiar entre disponible e inactivo
    if producto.estado == 'disponible':
        producto.estado = 'inactivo'
        mensaje = "⚫ Producto desactivado"
    else:
        producto.estado = 'disponible'
        mensaje = "🟢 Producto activado"
    
    producto.save()
    messages.success(request, mensaje)
    
    next_url = request.POST.get('next', request.GET.get('next', 'productos:mis_productos'))
    return redirect(next_url)

@login_required
def productos_mas_vendidos(request):
    """Mostrar estadísticas de productos más vendidos del usuario"""
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante")
        return redirect('productos:explorar')
    
    productos_vendidos = Producto.objects.filter(
        vendedor=request.user.estudiante,
        estado='vendido'
    ).order_by('-publicado_en')
    
    total_ventas = productos_vendidos.count()
    ingresos_totales = productos_vendidos.aggregate(Sum('precio'))['precio__sum'] or 0
    
    ventas_por_categoria = productos_vendidos.values(
        'categoria__nombre'
    ).annotate(
        total=Count('id'),
        ingresos=Sum('precio')
    ).order_by('-total')
    
    context = {
        'productos_vendidos': productos_vendidos,
        'total_ventas': total_ventas,
        'ingresos_totales': ingresos_totales,
        'ventas_por_categoria': ventas_por_categoria,
        'titulo': 'Mis Ventas'
    }
    return render(request, 'productos/ventas.html', context)