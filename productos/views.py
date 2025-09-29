from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Vista para explorar productos
@login_required
def explorar(request):
    # Datos de ejemplo - luego los reemplazarás con tu base de datos
    productos_ejemplo = [
        {
            'id': 1,
            'nombre': 'Libro de Matemáticas',
            'precio': 25.00,
            'descripcion': 'Libro de cálculo diferencial en excelente estado',
            'vendedor': 'Juan Pérez',
            'imagen': None
        },
        {
            'id': 2,
            'nombre': 'Calculadora Científica',
            'precio': 45.50,
            'descripcion': 'Calculadora TI-84 casi nueva',
            'vendedor': 'María García',
            'imagen': None
        },
        {
            'id': 3,
            'nombre': 'Laptop Dell',
            'precio': 1200.00,
            'descripcion': 'Laptop para estudios, 8GB RAM, 256GB SSD',
            'vendedor': 'Carlos López',
            'imagen': None
        },
        {
            'id': 4,
            'nombre': 'Bicicleta de Montaña',
            'precio': 300.00,
            'descripcion': 'Bicicleta usada pero en buen estado',
            'vendedor': 'Ana Martínez',
            'imagen': None
        },
    ]
    
    context = {
        'productos': productos_ejemplo,
        'titulo': 'Explorar Productos'
    }
    return render(request, 'productos/explorar.html', context)

# Vista para vender productos
@login_required
def vender(request):
    if request.method == 'POST':
        # Aquí procesarías el formulario de venta
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        
        # Lógica para guardar el producto (por ahora solo mensaje)
        messages.success(request, f'Producto "{nombre}" publicado exitosamente!')
        return redirect('explorar')
    
    context = {
        'titulo': 'Vender Producto'
    }
    return render(request, 'productos/vender.html', context)

# Vista para el perfil (puedes mover esta a usuarios si prefieres)
@login_required
def perfil(request):
    # Productos del usuario actual (ejemplo)
    mis_productos = [
        {
            'id': 1,
            'nombre': 'Libro de Física',
            'precio': 30.00,
            'descripcion': 'Libro de física universitaria',
            'imagen': None
        },
        {
            'id': 2,
            'nombre': 'Mouse Gaming',
            'precio': 35.00,
            'descripcion': 'Mouse RGB en perfecto estado',
            'imagen': None
        },
    ]
    
    context = {
        'productos': mis_productos,
        'titulo': 'Mi Perfil'
    }
    return render(request, 'productos/perfil.html', context)

# Vista simple para la página principal
def index(request):
    if request.user.is_authenticated:
        return redirect('explorar')
    else:
        return redirect('login')