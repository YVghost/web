from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Estudiante, Calificacion
from .forms import RegistroEstudianteForm, CalificacionForm

## REGISTRO
def registro(request):
    if request.method == "POST":
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            
            # Autenticar automáticamente al usuario
            user = authenticate(
                username=form.cleaned_data['correo'],
                password=form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                messages.success(request, "¡Cuenta creada exitosamente! 🎉")
                return redirect("productos:explorar")
            
    else:
        form = RegistroEstudianteForm()
    
    return render(request, "usuarios/registro.html", {"form": form})

## LOGIN
def login_estudiante(request):
    if request.method == "POST":
        # Usar 'username' y 'password' que espera Django
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Autenticar con el sistema seguro de Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido de vuelta, {user.first_name}! 👋")
            
            # Redirigir a la página que intentaba ver (si existe)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect("productos:explorar")
        else:
            messages.error(request, "❌ Correo o contraseña incorrectos")
    
    return render(request, "usuarios/login.html")

## LOGOUT
def logout_estudiante(request):
    logout(request)
    messages.success(request, "✅ Has cerrado sesión exitosamente")
    return redirect("productos:explorar")

## PERFIL
@login_required
def perfil(request, id=None):
    """Vista del perfil del usuario"""
    # Si no se proporciona id, usar el del usuario actual
    if id is None:
        try:
            estudiante = request.user.estudiante
            # Redirigir a la URL con el id
            return redirect('usuarios:perfil_con_id', id=estudiante.id)
        except Estudiante.DoesNotExist:
            messages.error(request, "Primero debes completar tu perfil de estudiante")
            return redirect('usuarios:registro')
    
    # Obtener el perfil del estudiante
    estudiante = get_object_or_404(Estudiante, id=id)
    
    # Verificar que el usuario tiene permiso para ver este perfil
    puede_editar = request.user == estudiante.user
    
    # Obtener calificaciones recientes
    calificaciones_recientes = estudiante.calificaciones_recibidas.all()[:5]
    
    context = {
        'estudiante': estudiante,
        'puede_editar': puede_editar,
        'calificaciones_recientes': calificaciones_recientes,
    }
    return render(request, 'usuarios/perfil.html', context)

## CALIFICAR VENDEDOR
@login_required
def calificar_vendedor(request, vendedor_id):
    """Calificar a un vendedor"""
    vendedor = get_object_or_404(Estudiante, id=vendedor_id)
    
    # Verificar que el usuario tenga perfil de estudiante
    if not hasattr(request.user, 'estudiante'):
        messages.error(request, "Debes tener un perfil de estudiante para calificar")
        return redirect('usuarios:perfil_con_id', id=vendedor.id)
    
    calificador = request.user.estudiante
    
    # Verificar si puede calificar
    if not calificador.puede_calificar(vendedor):
        messages.error(request, "No puedes calificar a este usuario")
        return redirect('usuarios:perfil_con_id', id=vendedor.id)
    
    # Verificar si ya ha calificado
    calificacion_existente = Calificacion.objects.filter(
        calificador=calificador,
        calificado=vendedor
    ).first()
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion_existente)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.calificador = calificador
            calificacion.calificado = vendedor
            
            calificacion.save()
            
            if calificacion_existente:
                messages.success(request, "✅ Calificación actualizada")
            else:
                messages.success(request, "⭐ Calificación enviada")
            
            return redirect('usuarios:perfil_con_id', id=vendedor.id)
    else:
        form = CalificacionForm(instance=calificacion_existente)
    
    context = {
        'form': form,
        'vendedor': vendedor,
        'calificacion_existente': calificacion_existente,
    }
    return render(request, 'usuarios/calificar.html', context)

## VER CALIFICACIONES
@login_required
def ver_calificaciones(request, estudiante_id):
    """Ver todas las calificaciones de un estudiante"""
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    calificaciones = estudiante.calificaciones_recibidas.all()
    
    # Asegurarse de que las estadísticas se calculen correctamente
    total_calificaciones = calificaciones.count()
    
    # Calcular distribución
    distribucion = {
        5: calificaciones.filter(estrellas=5).count(),
        4: calificaciones.filter(estrellas=4).count(),
        3: calificaciones.filter(estrellas=3).count(),
        2: calificaciones.filter(estrellas=2).count(),
        1: calificaciones.filter(estrellas=1).count(),
    }
    
    estadisticas = {
        'total': total_calificaciones,
        'promedio': estudiante.promedio_calificaciones or 0,
        'distribucion': distribucion
    }
    
    print("🔍 DEBUG - Estadísticas:", estadisticas)  # Para ver en consola
    
    context = {
        'estudiante': estudiante,
        'calificaciones': calificaciones,
        'estadisticas': estadisticas,
    }
    return render(request, 'usuarios/calificaciones.html', context)